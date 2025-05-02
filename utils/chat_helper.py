from firebase_admin import firestore
db = firestore.client()

def get_conversation_id(user1, user2):
    return "_".join(sorted([user1, user2]))

def send_message(sender, receiver, message):
    convo_id = get_conversation_id(sender, receiver)
    doc_ref = db.collection("messages").document(convo_id)
    doc = doc_ref.get()
    
    if doc.exists:
        messages = doc.to_dict().get("messages", [])
    else:
        messages = []
    
    messages.append({
        "from": sender,
        "to": receiver,
        "text": message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    doc_ref.set({"messages": messages})

def get_messages(user1, user2):
    convo_id = get_conversation_id(user1, user2)
    doc = db.collection("messages").document(convo_id).get()
    if doc.exists:
        return doc.to_dict().get("messages", [])
    return []
