import mysql.connector as mysql


#@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return mysql.connect(**st.secrets["mysql"])
