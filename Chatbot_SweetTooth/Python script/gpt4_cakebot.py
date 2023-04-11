import mysql.connector

def get_gpt4_Response(text):    
    mydb = mysql.connector.connect(
        host="cloud.mindsdb.com",
        user="parthjain1812@gmail.com",
        password='12345678',
        port="3306"
    )

    cursor = mydb.cursor()
    cursor.execute(f'''SELECT response FROM mindsdb.cakeshop_chatbot WHERE text = "{text}"''')

    return(cursor.fetchone()[0])

