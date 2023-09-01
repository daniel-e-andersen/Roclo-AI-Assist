# Delete chat histories and re-create the tables for chat history management.
from logger import setup_logger
from core import DynamoDBChatHistoryManager

try:
    # Initialize the logger.
    setup_logger()

    DynamoDBChatHistoryManager().connect()
except Exception as e:
    print(e)
    exit()


def main():
    # Delete all tables for chat history management.
    DynamoDBChatHistoryManager.reset_tables()




if __name__ == "__main__":
    main()