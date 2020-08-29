import jsonpickle
import redis

r=redis.Redis()
data_manager={
    "fruit": "Apple",
    "size": "Large",
    "color": "Red"
}
keyword_manager={
    "quiz": {
        "sport": {
            "q1": {
                "question": "Which one is correct team name in NBA?",
                "options": [
                    "New York Bulls",
                    "Los Angeles Kings",
                    "Golden State Warriros",
                    "Huston Rocket"
                ],
                "answer": "Huston Rocket"
            }
        },
        "maths": {
            "q1": {
                "question": "5 + 7 = ?",
                "options": [
                    "10",
                    "11",
                    "12",
                    "13"
                ],
                "answer": "12"
            },
            "q2": {
                "question": "12 - 8 = ?",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "answer": "4"
            }
        }
    }
}
config_manager={
    "quiz": {
        "sport": {
            "q1": {
                "question": "Which one is correct team name in NBA?",
                "options": [
                    "New York Bulls",
                    "Los Angeles Kings",
                    "Golden State Warriros",
                    "Huston Rocket"
                ],
                "answer": "Huston Rocket"
            }
        },
        "maths": {
            "q1": {
                "question": "5 + 7 = ?",
                "options": [
                    "10",
                    "11",
                    "12",
                    "13"
                ],
                "answer": "12"
            },
            "q2": {
                "question": "12 - 8 = ?",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "answer": "4"
            }
        }
    }
}
def save_data(data_manager,keyword_manager,config_manager):
    if r.set("data_manager",jsonpickle.dumps(data_manager)) and r.set("keyword_manager",jsonpickle.dumps(keyword_manager)) and r.set("config_manager",jsonpickle.dumps(config_manager)):
        r.mset({"data_manager":jsonpickle.dumps(data_manager),"keyword_manager":jsonpickle.dumps(keyword_manager),"config_manager":jsonpickle.dumps(config_manager)})
    else:
        print("Error to connect to Redis. Check Redis server")

save_data(data_manager,keyword_manager,config_manager)

def data_test():
        if r.get("data_manager") and r.get("config_manager") and r.get("keyword_manager"):
            return jsonpickle.decode(r.get("data_manager")),jsonpickle.decode(r.get("config_manager")),jsonpickle.decode(r.get("keyword_manager"))
            print(OK)
        else:
            print("Error to connect to Redis. Check Redis server")

a,b,c=data_test()
print(a,b,c)
