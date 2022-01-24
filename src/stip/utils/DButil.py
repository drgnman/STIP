import mysql.connector

class DBUtil:
  def __init__(self):
    self.host = 'localhost'
    self.database = 'SDS_SCHEMA'
    self.user = 'sdsuser',
    self.password = 'sdspassword0'
    self.connector = None
    self.cursor = None

  def createDBConnection(self):
    self.connector = mysql.connector.connect(
      user=self.user,
      password=self.password,
      host=self.host,
      database=self.database,
      auth_plugin='mysql_native_password'
    )
    self.cursor = self.connector.cursor()

  def closeDBConnection(self):
    self.cursor.close()
    self.connector.close()

  def executeQuery(self, sql):
    try:
      self.connector.autocommit = False
      self.cursor.execute(sql)
      self.connector.commit()
      return True

    except Exception as e:
      self.connector.roollback()
      print("SQL Execution ERROR!")
      print(str(e))
      return False

  def fetchAllQuery(self, sql):
    try:
      self.cursor.execute(sql)
      return self.cursor.fetchall()

    except Exception as e:
      print("Fetch Error!")
      print(str(e))
      return False

  def fetchSingleQuery(self, sql):
    try:
      self.cursor.execute(sql)
      result = self.cursor.fetchone()
      return result[0]

    except Exception as e:
      print("Fetch Error!")
      print(str(e))
      return False
