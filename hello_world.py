from __future__ import print_function

# We'll start with a couple of globals...
CardTitlePrefix = "(Pant) Suit Up"
AskQuestionIntent = "Good question"
Questions = ["Give me an example of when you showed initiative",
            "Tell me about a time you failed",
            "How would your friends describe you?",
            "Tell me about yourself",
            "Did you ever make a risky decision? Why? How did you handle it?"]
Sequences = [("Hi", "Bye")]
FeedbackTemplate = "Good job" #make this an object -- configure individual measure values--> call method to insert them


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Build a speechlet JSON representation of the title, output text, 
    reprompt text & end of session
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': CardTitlePrefix + " - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    """
    Build the full response JSON from the speechlet response
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

def begin_interview():

    # initialize interview variables
    intro, conclusion = pick_sequences()
    questions = pick_questions()
    session_attributes = {"current_question_index": 1,
                      "questions": questions,
                      "all_answers": "",
                      "conclusion": conclusion
                     }

    # initialize response variables
    card_title = "Beginning Interview"
    speech_output = "Welcome to (Pant) Suit Up. You're interview is beginning in 3, 2, 1, now! " + intro + " " + questions[0]
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, "no reprompt", should_end_session))

def handle_session_end_request(session):
    card_title = "Interview Done"
    speech_output = construct_feedback(session)

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def pick_questions():
    """
    Pick questions based on expected length of response and other factors in tags
    """
    return Questions[0:2]

def pick_sequences():
    """
    Pick opening/closing sequence pair randomly
    """
    return Sequences[0]

def construct_feedback(session):
    """
    Construct feedback from total answers
    """
    total_text = session["attributes"]["all_answers"]
    return FeedbackTemplate

def ask_question(intent, session):
    """
    Record answer in session attributes and ask new question or conclude interview
    """

    # update cumulative interview answer
    answer = intent['slots'].get('Answer', {}).get('value') # does this work for us?????
    session["attributes"]["all_answers"] += (" " + answer)

    # extract next question
    questions = session["attributes"]["questions"]
    question_index = session["attributes"]["current_question_index"]
    if question_index >= len(questions):
        return handle_session_end_request(session) # it's a wrap!
    question_string = questions[question_index]
    session["attributes"]["current_question_index"] += 1

    card_title = "Question"
    reprompt_text = "I'm sorry, but I didn't understand your answer. Can you try again?"
    return build_response({}, build_speechlet_response(card_title, question_string, reprompt_text, True))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return begin_interview()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    if intent_name == AskQuestionIntent:
        return ask_question(intent, session)
    elif intent_name == "AMAZON.StartOverIntent": # based on example ???
        return begin_interview()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(session)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])