"""
This is a simple Alexa Skill that gets you information about workshops at an event.
"""
from __future__ import print_function
import random

facts = [
    "This iconic building, designed in the 1960s by Eero Saarinen, once housed some of the best minds in science who performed fundamental work on communications systems.",
    "Bell Labs was home to ingenious minds that contributed to some of the greatest technological advancements of the twentieth century.",
    "8 Nobel Prizes Won",
    "Bell Labs was the best-funded and most successful corporate research laboratory the world has ever seen.",
    "At the Holmdel site alone, Bell researchers invented the cell phone and discovered background radiation, a critical step in the development of the Big Bang hypothesis."
]

dict = {
        'amazon': "At 7 pm today, Come say hello to me at the Alexa workshop. Learn how to build skills and integrate me into a Raspberry Pi. It'll be fun. I promise.", 
        'viacom': "At 8 pm today, bridging the Tech Gap Between Graduation and Your First Job by Viacom", 
        'twilio': "At 2 pm today, start building with Sync, Twihlio's newest API for synchronizing state across devices & users.",
        'ebay':   "At 3 pm today, from Java to Node: eBay's journey and tools for building web sites, FAST by eBay",
        'dell':   "At 1 am sunday morning, cup Stacking Hosted By Dell"
        }


# Populate with your skill's application ID to prevent someone else from
# configuring a skill that sends requests to this function.
APP_ID = ""

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if APP_ID and (event['session']['application']['applicationId'] != APP_ID):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    # return getWorkshopInfo(intent, session)
    return getWelcomeMessage()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetWorkshopInfoIntent":
        return getWorkshopInfo(intent, session)
    elif intent_name == "GetFactIntent":
        return getNewFact()
    elif intent_name == "AMAZON.StopIntent":
        return getGoodByeMessage()                
    elif intent_name == "AMAZON.CancelIntent":
        return getGoodByeMessage()        
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------

def getWelcomeMessage():
    card_title = "MLH Prime @ Bell Works"
    session_attributes = {}
    should_end_session = False
    
    fact = "Welcome to Major League Hacking Prime at Bell Works. The Bell Labs Holmdel Complex functioned for forty-four years as a research and development facility, initially for the Bell System. I am so excited to be here."
    speech_output = fact
    reprompt_text = "You can ask me for another fact about Bell Works by saying - tell me more"

    return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))

def getGoodByeMessage():
    card_title = "MLH Prime @ Bell Works"
    session_attributes = {}
    should_end_session = True
    
    fact = "Good Bye. I can't wait to see what you all build in the next 24 hours at this iconic venue. Happy hacking!"
    speech_output = fact
    reprompt_text = None

    return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))

    
def getNewFact():
    card_title = "MLH Prime @ Bell Works"
    session_attributes = {}
    should_end_session = False

    fact = facts[random.randint(0,len(facts))]
    speech_output = fact
    reprompt_text = "You can ask me for another fact about Bell Works by saying - tell me more about bell works"

    return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))

def getWorkshopInfo(intent,session):
    card_title = "MLH"
    session_attributes = {}
    should_end_session = False
    
    if 'Company' in intent['slots']:
        print("company was found")
        company_name = (intent['slots']['Company']['value']).lower()
        print("printing company name now......")
        print(dict[company_name])
        workshop_details = dict[company_name]
        speech_output = workshop_details
        # reprompt_text = None
        reprompt_text = "You can ask me about workshops at MLH by saying, " \
                        "What time is the workshop for Amazon?"
    else:
        print("company was not found")
        speech_output = "I'm not sure about that workshop." \
                        "Please try again."
        reprompt_text = "You can ask me about workshops at MLH by saying, " \
                        "What time is the workshop for Amazon?"

    return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------
        

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
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
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }