"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import logging
import json
import urllib2


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "<speak>Welcome to Tech Em Mission Control. " \
                    "Begin a model rocket launch by saying, " \
                    "Prepare for launch!</speak>"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "To launch your model rocket say, " \
                    "Prepare for launch."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "<speak>Launch aborted and scrubbed. Please check the area and re-arm when ready to re-commence. </speak>"

    mesg = "disarm"
    
    slack_mesg = { 'channel':'#mission_control','username':'sirexa','text':mesg}
    resp = urllib2.urlopen('https://hooks.slack.com/services/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',json.dumps(slack_mesg))


    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def arm(intent, session):
    """ Arm for launch.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "<speak>Arming for Launch.</speak>"
                        
    reprompt_text = "All systems not clear. Please try again."
    
    mesg = "Please arm-1123"
    
    slack_mesg = { 'channel':'#mission_control','username':'sirexa','text':mesg}
    resp = urllib2.urlopen('https://hooks.slack.com/services/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',json.dumps(slack_mesg))

    session_attributes['state'] = 'arm'
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def commence_launch(intent, session):
    """ Start the launch sequence.
    """

    card_title = intent['name']
    session_attributes = session['attributes'] if session.has_key('attributes') else {}
    should_end_session = False

    if session_attributes.has_key('state') and session_attributes['state'] == 'arm':
        speech_output = "<speak>Launch sequence commencing. T minus 10,<break time='650ms'/> 9,<break time='650ms'/> 8,<break time='650ms'/> 7,<break time='650ms'/> 6,<break time='750ms'/> 5,<break time='650ms'/> Confirm all systems go.</speak>"
        session_attributes['state'] = 'countdown'
        mesg = "Please commence pre-launch-sequence-1123"
        slack_mesg = { 'channel':'#mission_control','username':'sirexa','text':mesg}
        resp = urllib2.urlopen('https://hooks.slack.com/services/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',json.dumps(slack_mesg))

    else:
        speech_output = "<speak>Ignition system must be armed prior to launch sequence.</speak>"
                        
    reprompt_text = "All systems not clear. Please try again."
    

    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def confirm_launch(intent, session):
    """ Start the launch sequence.
    """

    card_title = intent['name']
    session_attributes = session['attributes'] if session.has_key('attributes') else {}
    should_end_session = True

    if session_attributes.has_key('state') and session_attributes['state'] == 'countdown':
        speech_output = "<speak>three, <break time='650ms'/> two,<break time='650ms'/> one,<break time='650ms'/>. <say-as interpret-as='interjection'>Blast Off!.</say-as></speak>"
        mesg = "Please commence launch-1123"
        slack_mesg = { 'channel':'#mission_control','username':'sirexa','text':mesg}
        resp = urllib2.urlopen('https://hooks.slack.com/services/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',json.dumps(slack_mesg))

    else:
        speech_output = "<speak>Ignition systems must be armed, and launch sequence started, prior to launch.</speak>"
                        
    reprompt_text = "All systems not clear. Please try again."
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

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
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Arm":
        return arm(intent,session)
    elif intent_name == "LaunchMyRocket":
        return commence_launch(intent, session)
    elif intent_name == "ConfirmLaunch":
        return confirm_launch(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
