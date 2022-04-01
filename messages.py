from db import db
import users


def get_list():
    sql = "SELECT M.message, U.username, M.sent_at FROM messages M, users U " \
          "WHERE M.user_id=U.id ORDER BY M.sent_at DESC"
    result = db.session.execute(sql)
    return result.fetchall()


def send(message):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (message, user_id, sent_at) VALUES (:message, :user_id, NOW()::timestamp(0))"
    db.session.execute(sql, {"message": message, "user_id": user_id})
    db.session.commit()
    return True


def search(query):
    try:
        # To fix FlAW 3 uncomment the three lines below
        # sql = "SELECT M.message, U.username, M.sent_at FROM messages M, users U " \
        #       "WHERE M.user_id=U.id AND M.message LIKE :query"
        # query_result = db.session.execute(sql, {"query": query})

        # To fix FlAW 3 comment/remove the three lines below
        sql = "SELECT M.message, U.username, M.sent_at FROM messages M, users U " \
              "WHERE M.user_id=U.id AND M.message LIKE \'%" + query + "%\'"
        query_result = db.session.execute(sql)

        messages = query_result.fetchall()
        if len(messages) == 0:
            not_found_message = [("No messages found",), ]
            return not_found_message
        return messages
    except:
        error_message = [("ERROR!",), ]
        return error_message
