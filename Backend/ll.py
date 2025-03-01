#!/usr/bin/env python
# coding: utf-8

import json
import math
import os
import requests
import sys
import time
import threading
import wave

import numpy as np
import soundfile as sf

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    sys.exit(1)

# Set up the subscription info for the Speech Service
speech_key, service_region = "38d3ad0237484649901bdf105bfaffee", "eastus"

# Set up the parameters for Gemini API
gemini_api_url = "https://api.gemini.com/v1/your-endpoint"
gemini_api_key = "AIzaSyDQ4yAsKyz6_z9ypE7B2OzW0b3oeiwByvk"

sample_width = 2
sample_rate = 16000
channels = 1
reduced_unit = 10000000

def read_wave_header(file_path):
    with wave.open(file_path, 'rb') as audio_file:
        framerate = audio_file.getframerate()
        bits_per_sample = audio_file.getsampwidth() * 8
        num_channels = audio_file.getnchannels()
        return framerate, bits_per_sample, num_channels

def push_stream_writer(stream, filenames, merged_audio_path):
    byte_data = b""
    n_bytes = 3200
    try:
        for filename in filenames:
            wav_fh = wave.open(filename)
            try:
                while True:
                    frames = wav_fh.readframes(n_bytes // 2)
                    if not frames:
                        break
                    stream.write(frames)
                    byte_data += frames
                    time.sleep(.1)
            finally:
                wav_fh.close()
        with wave.open(merged_audio_path, 'wb') as wave_file:
            wave_file.setnchannels(channels)
            wave_file.setsampwidth(sample_width)
            wave_file.setframerate(sample_rate)
            wave_file.writeframes(byte_data)
    finally:
        stream.close()

def merge_wav(audio_list, output_path, tag=None):
    combined_audio = np.empty((0,))
    for audio in audio_list:
        y, _ = sf.read(audio, dtype="float32")
        combined_audio = np.concatenate((combined_audio, y))
        os.remove(audio)
    sf.write(output_path, combined_audio, sample_rate)
    if tag:
        print(f"Save {tag} to {output_path}")

def get_mispronunciation_clip(offset, duration, save_path, merged_audio_path):
    y, _ = sf.read(
        merged_audio_path,
        start=int((offset) / reduced_unit * sample_rate),
        stop=int((offset + duration) / reduced_unit * sample_rate),
        dtype=np.float32
    )
    sf.write(save_path, y, sample_rate)

def strip_end_silence(file_path):
    y, _ = sf.read(file_path, start=0, stop=-int(sample_rate*0.8), dtype=np.float32)
    sf.write(file_path, y, sample_rate)

def chatting_from_file():
    """Performs chatting with Gemini and Azure Pronunciation Assessment asynchronously from audio files."""

    topic = "describe working dogs"
    input_files = ["resources/chat_input_1.wav", "resources/chat_input_2.wav"]
    reference_text = ""

    def stt(filename):
        result_text = []

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_config = speechsdk.audio.AudioConfig(filename=filename)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt: speechsdk.SessionEventArgs):
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(lambda evt: result_text.append(evt.result.text))
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        nonlocal reference_text
        speech_recognizer.stop_continuous_recognition()
        text = " ".join(result_text)
        reference_text += text + " "
        print("YOU: ", text)
        return text

    def call_gemini(send_text):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {gemini_api_key}"}
        data = {"input": send_text}

        response = requests.post(gemini_api_url, headers=headers, json=data)
        response.raise_for_status()
        text = response.json()["output"]
        print("Gemini: ", text)
        return text

    def tts(text, output_path, tag=None):
        # Instead of generating audio, return the text directly
        print(f"Text output: {text}")
        return text

    def pronunciation_assessment():
        framerate, bits_per_sample, num_channels = read_wave_header(input_files[0])
        format = speechsdk.audio.AudioStreamFormat(
            samples_per_second=framerate,
            bits_per_sample=bits_per_sample,
            channels=num_channels
        )
        stream = speechsdk.audio.PushAudioInputStream(format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        json_string = {
            "GradingSystem": "HundredMark",
            "Granularity": "Phoneme",
            "EnableMiscue": False,
            "phonemeAlphabet": "IPA",
        }
        pronunciation_config = speechsdk.PronunciationAssessmentConfig(json_string=json.dumps(json_string))
        pronunciation_config.enable_prosody_assessment()
        pronunciation_config.enable_content_assessment_with_topic(topic)
        pronunciation_config.reference_text = reference_text.strip()

        language = 'en-US'
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            language=language,
            audio_config=audio_config
        )
        pronunciation_config.apply_to(speech_recognizer)

        done = False
        recognized_words = []
        prosody_scores = []
        fluency_scores = []
        durations = []
        results = []
        json_words = []
        display_text = ""

        def stop_cb(evt):
            nonlocal done
            done = True

        def recognized(evt):
            pronunciation_result = speechsdk.PronunciationAssessmentResult(evt.result)
            nonlocal recognized_words, prosody_scores, fluency_scores, durations, results, json_words, display_text
            results.append(pronunciation_result)
            recognized_words += pronunciation_result.words
            fluency_scores.append(pronunciation_result.fluency_score)
            json_result = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
            jo = json.loads(json_result)
            nb = jo["NBest"][0]
            display_text += nb["Display"]
            json_words += nb["Words"]
            prosody_scores.append(pronunciation_result.prosody_score)
            durations.append(sum([int(w["Duration"]) for w in nb["Words"]]))

        speech_recognizer.recognized.connect(recognized)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        merged_audio_path = "output/merged_audio.wav"
        push_stream_writer_thread = threading.Thread(target=push_stream_writer, args=[stream, input_files, merged_audio_path])
        push_stream_writer_thread.start()
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()
        push_stream_writer_thread.join()

        final_accuracy_scores = []
        for word in recognized_words:
            if word.error_type == 'Insertion':
                continue
            else:
                final_accuracy_scores.append(word.accuracy_score)
        accuracy_score = sum(final_accuracy_scores) / len(final_accuracy_scores)

        if len(prosody_scores) == 0:
            prosody_score = float("nan")
        else:
            prosody_score = sum(prosody_scores) / len(prosody_scores)

        fluency_score = sum([x * y for (x, y) in zip(fluency_scores, durations)]) / sum(durations)

        pron_score = accuracy_score * 0.6 + fluency_score * 0.2 + prosody_score * 0.2
        print(f"Pronunciation score: {pron_score:.1f}")
        print(f"Accuracy Score: {accuracy_score:.1f}")
        if not math.isnan(prosody_score):
            print(f"Prosody Score: {prosody_score:.1f}")
        print(f"Fluency Score: {fluency_score:.1f}")
        assert results[-1].content_assessment_result is not None
        content_result = results[-1].content_assessment_result
        print(f"Vocabulary score: {content_result.vocabulary_score:.1f}")
        print(f"Grammar score: {content_result.grammar_score:.1f}")
        print(f"Topic score: {content_result.topic_score:.1f}")

        comment_result(
            {
                "accuracy score": accuracy_score,
                "fluency score": fluency_score,
                "prosody score": prosody_score,
                "vocabulary score": content_result.vocabulary_score,
                "grammar score": content_result.grammar_score,
                "topic score": content_result.topic_score
            },
            set_punctuation(json_words, display_text),
            [
                word for word in json_words
                if word["PronunciationAssessment"]["ErrorType"] == "Mispronunciation"
                or word["PronunciationAssessment"]["AccuracyScore"] < 60
            ],
            merged_audio_path
        )

    def set_punctuation(json_words, display_text):
        for idx, word in enumerate(display_text.split(" ")):
            if not word[-1].isalpha() and not word[-1].isdigit():
                json_words[idx]["is_punctuation"] = True
        return json_words

    def comment_result(scores_dict, json_words, mis_pronunciation_words, merged_audio_path):
        message_dict = {
            "Excellent": [],
            "Good": [],
            "Fair": [],
            "Poor": [],
            "Bad": [],
        }
        error_dict = {
            "Missing break": [],
            "Unexpected break": [],
            "Monotone": [],
        }

        def set_message_dict(score, score_name):
            if score >= 80:
                return message_dict["Excellent"].append(score_name)
            elif score < 80 and score >= 60:
                return message_dict["Good"].append(score_name)
            elif score < 60 and score >= 40:
                return message_dict["Fair"].append(score_name)
            elif score < 40 and score >= 20:
                return message_dict["Poor"].append(score_name)
            else:
                return message_dict["Bad"].append(score_name)

        def get_prosody_error(error_type, word, last_word):
            threshold = 0.1
            if error_type == "MissingBreak" or error_type == "UnexpectedBreak":
                break_error_info = \
                    word["PronunciationAssessment"]["Feedback"]["Prosody"]["Break"].get(error_type, "null")
                if break_error_info == "null":
                    return False
                if error_type == "MissingBreak":
                    if break_error_info["Confidence"] >= threshold and last_word.get("is_punctuation", False):
                        return True
                if error_type == "UnexpectedBreak":
                    if break_error_info["Confidence"] >= threshold and not last_word.get("is_punctuation", False):
                        return True
                return False
            elif error_type == "Monotone" and \
                    error_type in word["PronunciationAssessment"]["Feedback"]["Prosody"]["Intonation"]["ErrorTypes"]:
                return True
            else:
                return False

        def set_error_dict(json_words):
            for idx, word in enumerate(json_words):
                if get_prosody_error("MissingBreak", word, json_words[idx-1]):
                    error_dict["Missing break"].append(word)
                elif get_prosody_error("UnexpectedBreak", word, json_words[idx-1]):
                    error_dict["Unexpected break"].append(word)
                elif get_prosody_error("Monotone", word, json_words[idx-1]):
                    error_dict["Monotone"].append(word)

        def get_error_message(error_types):
            message = ""
            for error_type in error_types:
                if len(error_dict[error_type]) != 0:
                    message += f"{error_type} count is {len(error_dict[error_type])}. near the word "
                    message += f"{' '.join([word['Word'].strip() for word in error_dict[error_type]])}. "

            return message

        def get_report(json_words, mis_pronunciation_words, merged_audio_path):

            set_error_dict(json_words)

            report_audio_list = []
            accuracy_report_audio_list = []
            report_path = "output/chat_report.wav"
            if len(mis_pronunciation_words) != 0:
                accuracy_report_path = "output/accuracy_report.wav"
                for idx, mis_word in enumerate(mis_pronunciation_words):
                    origin_content = ""
                    report_clip_path = f"output/accuracy_report_clip_{idx+1}.wav"
                    mis_word_clip_path = f"output/mis_word_clip_{idx+1}.wav"
                    if idx == 0:
                        origin_content += "Accuracy report:"
                    origin_content += f' word {mis_word["Word"]}'
                    origin_content += f' correct pronunciation is {mis_word["Word"]}, your pronunciation is'

                    tts(origin_content, report_clip_path)
                    get_mispronunciation_clip(
                        mis_word["Offset"],
                        mis_word["Duration"],
                        mis_word_clip_path,
                        merged_audio_path
                    )
                    accuracy_report_audio_list.append(report_clip_path)
                    accuracy_report_audio_list.append(mis_word_clip_path)
                merge_wav(accuracy_report_audio_list, accuracy_report_path)
                report_audio_list.append(accuracy_report_path)
                os.remove(merged_audio_path)

            if scores_dict["fluency score"] < 60 or scores_dict["prosody score"] < 60:
                origin_content = ""
                fluency_prosody_report_path = "output/fluency_prosody_report.wav"
                if scores_dict["fluency score"] < 60:
                    origin_content += "Fluency "
                if scores_dict["prosody score"] < 60:
                    origin_content += "Prosody "
                origin_content += "report: "
                origin_content += get_error_message(["Missing break", "Unexpected break", "Monotone"])

                tts(origin_content, fluency_prosody_report_path)
                report_audio_list.append(fluency_prosody_report_path)

            merge_wav(report_audio_list, report_path, "report")

        def get_score_comment(scores_dict):
            for score_key in scores_dict:
                set_message_dict(scores_dict[score_key], score_key)

            messages = ""
            for message_key in message_dict:
                if message_dict[message_key] != []:
                    is_or_are = "is" if len(message_dict[message_key]) == 1 else "are"
                    messages += f"{', '.join(message_dict[message_key])} {is_or_are} {message_key}. "

            tts(messages, "output/chat_score_comment.wav", "score comment")

        get_score_comment(scores_dict)
        get_report(json_words, mis_pronunciation_words, merged_audio_path)

    if not os.path.exists("output"):
        os.makedirs("output")
    for idx, file in enumerate(input_files):
        tts(call_gemini(stt(file)), f"output/gpt_output_{idx+1}.wav", "GPT output")
    print("Generate the final report ......")
    pronunciation_assessment()

if __name__ == "__main__":
    chatting_from_file()