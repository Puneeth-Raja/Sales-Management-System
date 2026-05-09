import streamlit as st
import db
import mysql.connector


def login():

    # Center the login form
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        st.markdown(
            """
            <h2 style='text-align:center; margin-bottom:30px;'>
                Sales Intelligence Hub
            </h2>
            """,
            unsafe_allow_html=True
        )

        # Style Streamlit form directly
        st.markdown("""
            <style>
            div[data-testid="stForm"] {
                background-color: #f8f9fa;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            }
            </style>
        """, unsafe_allow_html=True)

        with st.form('login_form'):

            st.subheader("Login")

            username = st.text_input('Username')
            password = st.text_input('Password', type='password')

            submit = st.form_submit_button(
                'Login',
                use_container_width=True
            )

            if submit:

                conn = None
                cur = None

                try:
                    conn = db.get_connection()
                    cur = conn.cursor(dictionary=True)

                    query = '''
                        SELECT * FROM users
                        WHERE username=%s AND password=%s
                    '''

                    cur.execute(query, (username, password))

                    user = cur.fetchone()

                except mysql.connector.Error as e:
                    st.error(f'Database Error: {e}')
                    return

                finally:
                    if cur:
                        cur.close()

                    if conn:
                        conn.close()

                if user:
                    st.session_state['Authenticated'] = True
                    st.session_state['user_details'] = user
                    st.rerun()

                else:
                    st.error('Invalid Username or Password')