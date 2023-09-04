# database.py
import os
import mysql.connector

DATABASE_NAME = 'celagia'

def set_env_variable(key, value):
    with open(os.path.expanduser("~/.bashrc"), "a") as f:
        f.write(f"\nexport {key}='{value}'")
    os.system("source ~/.bashrc")

class Database:

    def __init__(self, db_name=DATABASE_NAME, port=3306):
        self.db_name = db_name
        try:
            user = os.environ['CELAIGIA_USER']
            password = os.environ['CELAIGIA_PASSWORD']
        except KeyError:
            user = input("Enter your MySQL username: ")
            password = input("Enter your MySQL password: ")
            set_env_variable('CELAIGIA_USER', user)
            set_env_variable('CELAIGIA_PASSWORD', password)
            set_env_variable('CELAIGIA_PORT', port)

        self.db = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database=self.db_name,
            port = port
        )
        self.cursor = self.db.cursor()

    # def initialize_database(self):
    #     self.cursor.execute("SHOW DATABASES;")
    #     databases = [db[0] for db in self.cursor.fetchall()]
    #
    #     if self.db_name not in databases:
    #         self.cursor.execute(f"CREATE DATABASE {self.db_name};")
    #         print(f"Database {self.db_name} created.")
    #     else:
    #         print(f"Database {self.db_name} already exists.")
    #
    #     self.cursor.execute(f"USE {self.db_name};")
    #
    #     # Check if the download_logs table exists
    #     self.cursor.execute("SHOW TABLES LIKE 'download_logs';")
    #     if not self.cursor.fetchone():
    #         self.cursor.execute("""
    #             CREATE TABLE download_logs (
    #                 id INT AUTO_INCREMENT PRIMARY KEY,
    #                 video_title VARCHAR(255) NOT NULL,
    #                 video_url VARCHAR(512) NOT NULL,
    #                 video_query VARCHAR(255) NOT NULL,
    #                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    #             );
    #         """)
    #         print("Table download_logs created.")
    #     else:
    #         print("Table download_logs already exists.")
    #
    #     print("Database initialization complete!")

    def log_download(self, video_title, video_url, video_query=''):

        sql = "INSERT INTO download_logs (video_title, video_url, video_query) VALUES (%s, %s, %s);"
        val = (video_title, video_url, video_query)
        self.cursor.execute(sql, val)
        self.db.commit()

    def check_downloaded(self, video_url):
        sql = "SELECT video_url FROM download_logs WHERE video_url=%s;"
        val = (video_url,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result:
            return True
        return False

    # conda list environments:

    def close(self):
        self.cursor.close()
        self.db.close()


# This part is executed if the script is run directly
if __name__ == "__main__":
    db = Database()
    db.initialize_database()
    db.close()
