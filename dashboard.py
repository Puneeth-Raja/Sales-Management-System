import streamlit as st
import pandas as pd
import plotly.express as px
import db


def dashboard():

    # ---------------- DATABASE FUNCTIONS ---------------- #

    def fetch_dataframe(query, params=None):

        conn = db.get_connection()

        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)

        conn.close()

        return df


    def execute_query(query, values):

        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(query, values)

        conn.commit()

        cur.close()
        conn.close()


    # ---------------- USER SESSION ---------------- #

    user = st.session_state['user_details']

    role = user['role']
    branch_id = user['branch_id']
    username = user['username']


    # ---------------- SIDEBAR ---------------- #

    st.sidebar.markdown("## 📊 Sales Intelligence Hub")

    st.sidebar.success(f"Logged in as: {username}")
    st.sidebar.info(f"Role: {role}")

    menu = st.sidebar.radio(
        'Navigation',
        [
            'Dashboard',
            'Add Sales',
            'Add Payment',
            'Sales Report',
            'Pending Payments',
            'Analytics'
        ]
    )

    if st.sidebar.button('Logout', use_container_width=True):

        st.session_state['Authenticated'] = False
        st.session_state['user_details'] = None

        st.rerun()


    # ---------------- DASHBOARD ---------------- #

    if menu == 'Dashboard':

        st.title('📈 Sales Intelligence Dashboard')

        if role == 'Super Admin':

            kpi_query = '''
                SELECT
                IFNULL(SUM(gross_sales),0) total_sales,
                IFNULL(SUM(received_amount),0) total_received,
                IFNULL(SUM(pending_amount),0) total_pending
                FROM customer_sales
            '''

            trend_query = '''
                SELECT
                joining_date,
                SUM(gross_sales) total_sales
                FROM customer_sales
                GROUP BY joining_date
                ORDER BY joining_date
            '''

            branch_query = '''
                SELECT
                b.branch_name,
                SUM(c.gross_sales) total_sales
                FROM customer_sales c
                JOIN branches b
                ON c.branch_id = b.branch_id
                GROUP BY b.branch_name
            '''

            payment_query = '''
                SELECT
                payment_method,
                SUM(amount_paid) total_collection
                FROM payment_splits
                GROUP BY payment_method
            '''

            kpi_df = fetch_dataframe(kpi_query)
            trend_df = fetch_dataframe(trend_query)
            branch_df = fetch_dataframe(branch_query)
            payment_df = fetch_dataframe(payment_query)

        else:

            kpi_query = '''
                SELECT
                IFNULL(SUM(gross_sales),0) total_sales,
                IFNULL(SUM(received_amount),0) total_received,
                IFNULL(SUM(pending_amount),0) total_pending
                FROM customer_sales
                WHERE branch_id=%s
            '''

            trend_query = '''
                SELECT
                joining_date,
                SUM(gross_sales) total_sales
                FROM customer_sales
                WHERE branch_id=%s
                GROUP BY joining_date
                ORDER BY joining_date
            '''

            branch_query = '''
                SELECT
                b.branch_name,
                SUM(c.gross_sales) total_sales
                FROM customer_sales c
                JOIN branches b
                ON c.branch_id = b.branch_id
                WHERE c.branch_id=%s
                GROUP BY b.branch_name
            '''

            payment_query = '''
                SELECT
                ps.payment_method,
                SUM(ps.amount_paid) total_collection
                FROM payment_splits ps
                JOIN customer_sales cs
                ON ps.sale_id = cs.sale_id
                WHERE cs.branch_id=%s
                GROUP BY ps.payment_method
            '''

            kpi_df = fetch_dataframe(kpi_query, (branch_id,))
            trend_df = fetch_dataframe(trend_query, (branch_id,))
            branch_df = fetch_dataframe(branch_query, (branch_id,))
            payment_df = fetch_dataframe(payment_query, (branch_id,))

        total_sales = kpi_df.iloc[0]['total_sales']
        total_received = kpi_df.iloc[0]['total_received']
        total_pending = kpi_df.iloc[0]['total_pending']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                'Total Gross Sales',
                f"₹ {total_sales:,.0f}"
            )

        with col2:
            st.metric(
                'Received Amount',
                f"₹ {total_received:,.0f}"
            )

        with col3:
            st.metric(
                'Pending Amount',
                f"₹ {total_pending:,.0f}"
            )

        st.divider()

        chart1, chart2 = st.columns(2)

        with chart1:

            st.subheader('Sales Trend')

            fig1 = px.line(
                trend_df,
                x='joining_date',
                y='total_sales',
                markers=True
            )

            st.plotly_chart(fig1, use_container_width=True)

        with chart2:

            st.subheader('Branch Performance')

            fig2 = px.bar(
                branch_df,
                x='branch_name',
                y='total_sales'
            )

            st.plotly_chart(fig2, use_container_width=True)

        st.subheader('Payment Method Analysis')

        fig3 = px.pie(
            payment_df,
            names='payment_method',
            values='total_collection'
        )

        st.plotly_chart(fig3, use_container_width=True)


    # ---------------- ADD SALES ---------------- #

    elif menu == 'Add Sales':

        st.title('➕ Add New Sales Entry')

        branches_df = fetch_dataframe(
            'SELECT * FROM branches'
        )

        branch_options = dict(
            zip(
                branches_df['branch_name'],
                branches_df['branch_id']
            )
        )

        with st.form('sales_form', clear_on_submit=True):

            col1, col2 = st.columns(2)

            with col1:

                if role == 'Super Admin':

                    selected_branch = st.selectbox(
                        'Select Branch',
                        list(branch_options.keys())
                    )

                    selected_branch_id = branch_options[selected_branch]

                else:

                    selected_branch_id = branch_id

                    st.info(
                        'You can add sales only for your assigned branch.'
                    )

                joining_date = st.date_input('Joining Date')

                customer_name = st.text_input(
                    'Customer Name'
                )

                mobile_number = st.text_input(
                    'Mobile Number'
                )

            with col2:

                product_name = st.selectbox(
                    'Product Name',
                    ['DS', 'DA', 'BA', 'FSD']
                )

                gross_sales = st.number_input(
                    'Gross Sales Amount',
                    min_value=0.0,
                    step=100.0
                )

                # st.markdown('### Information')
                # st.write('• Pending amount auto-calculates')
                # st.write('• Status updates automatically')
                # st.write('• Triggers handle payment tracking')

            st.divider()

            submit = st.form_submit_button(
                'Add Sales Entry',
                use_container_width=True
            )

            if submit:

                query = '''
                    INSERT INTO customer_sales(
                        branch_id,
                        joining_date,
                        customer_name,
                        mobile_number,
                        product_name,
                        gross_sales,
                        received_amount,
                        status
                    )
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                '''

                values = (
                    selected_branch_id,
                    joining_date,
                    customer_name,
                    mobile_number,
                    product_name,
                    gross_sales,
                    0,
                    'Open'
                )

                try:

                    execute_query(query, values)

                    st.success(
                        'Sales Entry Added Successfully'
                    )

                    st.balloons()

                except Exception as e:

                    st.error(f'Error: {e}')


    # ---------------- ADD PAYMENT ---------------- #

    elif menu == 'Add Payment':

        st.title('💳 Add Payment Split')

        if role == 'Super Admin':

            query = '''
                SELECT
                sale_id,
                customer_name
                FROM customer_sales
            '''

            sales_df = fetch_dataframe(query)

        else:

            query = '''
                SELECT
                sale_id,
                customer_name
                FROM customer_sales
                WHERE branch_id=%s
            '''

            sales_df = fetch_dataframe(
                query,
                (branch_id,)
            )

        sales_options = {
            f"{row['sale_id']} - {row['customer_name']}": row['sale_id']
            for _, row in sales_df.iterrows()
        }

        with st.form('payment_form', clear_on_submit=True):

            selected_sale = st.selectbox(
                'Select Sale',
                list(sales_options.keys())
            )

            sale_id = sales_options[selected_sale]

            payment_date = st.date_input(
                'Payment Date'
            )

            amount_paid = st.number_input(
                'Amount Paid',
                min_value=0.0,
                step=100.0
            )

            payment_method = st.selectbox(
                'Payment Method',
                ['Cash', 'UPI', 'Card']
            )

            submit_payment = st.form_submit_button(
                'Add Payment',
                use_container_width=True
            )

            if submit_payment:

                query = '''
                    INSERT INTO payment_splits(
                        sale_id,
                        payment_date,
                        amount_paid,
                        payment_method
                    )
                    VALUES(%s,%s,%s,%s)
                '''

                values = (
                    sale_id,
                    payment_date,
                    amount_paid,
                    payment_method
                )

                try:

                    execute_query(query, values)

                    st.success(
                        'Payment Added Successfully'
                    )

                except Exception as e:

                    st.error(f'Error: {e}')


    # ---------------- SALES REPORT ---------------- #

    elif menu == 'Sales Report':

        st.title('📄 Sales Report')

        if role == 'Super Admin':

            query = '''
                SELECT
                c.sale_id,
                b.branch_name,
                c.joining_date,
                c.customer_name,
                c.mobile_number,
                c.product_name,
                c.gross_sales,
                c.received_amount,
                c.pending_amount,
                c.status
                FROM customer_sales c
                JOIN branches b
                ON c.branch_id = b.branch_id
                ORDER BY c.sale_id DESC
            '''

            df = fetch_dataframe(query)

        else:

            query = '''
                SELECT
                c.sale_id,
                b.branch_name,
                c.joining_date,
                c.customer_name,
                c.mobile_number,
                c.product_name,
                c.gross_sales,
                c.received_amount,
                c.pending_amount,
                c.status
                FROM customer_sales c
                JOIN branches b
                ON c.branch_id = b.branch_id
                WHERE c.branch_id=%s
                ORDER BY c.sale_id DESC
            '''

            df = fetch_dataframe(query, (branch_id,))

        st.dataframe(df, use_container_width=True)


    # ---------------- PENDING PAYMENTS ---------------- #

    elif menu == 'Pending Payments':

        st.title('⏳ Pending Payments')

        if role == 'Super Admin':

            query = '''
                SELECT
                sale_id,
                customer_name,
                gross_sales,
                received_amount,
                pending_amount,
                status
                FROM customer_sales
                WHERE pending_amount > 0
            '''

            df = fetch_dataframe(query)

        else:

            query = '''
                SELECT
                sale_id,
                customer_name,
                gross_sales,
                received_amount,
                pending_amount,
                status
                FROM customer_sales
                WHERE pending_amount > 0
                AND branch_id=%s
            '''

            df = fetch_dataframe(query, (branch_id,))

        st.dataframe(df, use_container_width=True)


    # ---------------- ANALYTICS ---------------- #

        # ---------------- ANALYTICS ---------------- #

    elif menu == 'Analytics':

        st.title('📊 Business Analytics')

        if role == 'Super Admin':

            analytics_queries = {

                'Total Gross Sales': '''
                    SELECT
                    SUM(gross_sales) total_gross_sales
                    FROM customer_sales
                ''',

                'Total Pending Amount': '''
                    SELECT
                    SUM(pending_amount) total_pending
                    FROM customer_sales
                ''',

                'Top 3 Highest Sales': '''
                    SELECT
                    sale_id,
                    customer_name,
                    gross_sales
                    FROM customer_sales
                    ORDER BY gross_sales DESC
                    LIMIT 3
                ''',

                'Branch Wise Sales': '''
                    SELECT
                    b.branch_name,
                    SUM(c.gross_sales) total_sales
                    FROM customer_sales c
                    JOIN branches b
                    ON c.branch_id = b.branch_id
                    GROUP BY b.branch_name
                ''',

                'Payment Method Analysis': '''
                    SELECT
                    payment_method,
                    SUM(amount_paid) total_collection
                    FROM payment_splits
                    GROUP BY payment_method
                ''',

                'Monthly Sales Summary': '''
                    SELECT
                    YEAR(joining_date) year,
                    MONTH(joining_date) month,
                    SUM(gross_sales) total_sales
                    FROM customer_sales
                    GROUP BY YEAR(joining_date), MONTH(joining_date)
                '''
            }

            selected_query = st.selectbox(
                'Select Analytics Query',
                list(analytics_queries.keys())
            )

            result_df = fetch_dataframe(
                analytics_queries[selected_query]
            )

        else:

            analytics_queries = {

                'Total Gross Sales': '''
                    SELECT
                    SUM(gross_sales) total_gross_sales
                    FROM customer_sales
                    WHERE branch_id=%s
                ''',

                'Total Pending Amount': '''
                    SELECT
                    SUM(pending_amount) total_pending
                    FROM customer_sales
                    WHERE branch_id=%s
                ''',

                'Top 3 Highest Sales': '''
                    SELECT
                    sale_id,
                    customer_name,
                    gross_sales
                    FROM customer_sales
                    WHERE branch_id=%s
                    ORDER BY gross_sales DESC
                    LIMIT 3
                ''',

                'Payment Method Analysis': '''
                    SELECT
                    ps.payment_method,
                    SUM(ps.amount_paid) total_collection
                    FROM payment_splits ps
                    JOIN customer_sales cs
                    ON ps.sale_id = cs.sale_id
                    WHERE cs.branch_id=%s
                    GROUP BY ps.payment_method
                ''',

                'Monthly Sales Summary': '''
                    SELECT
                    YEAR(joining_date) year,
                    MONTH(joining_date) month,
                    SUM(gross_sales) total_sales
                    FROM customer_sales
                    WHERE branch_id=%s
                    GROUP BY YEAR(joining_date), MONTH(joining_date)
                '''
            }

            selected_query = st.selectbox(
                'Select Analytics Query',
                list(analytics_queries.keys())
            )

            result_df = fetch_dataframe(
                analytics_queries[selected_query],
                (branch_id,)
            )

        st.dataframe(
            result_df,
            use_container_width=True
        )