# Code Clippy — Inline code suggestions from your friendly neighborhood hacker Clippy for VSCode

<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/ncoop57/gpt-code-clippy/camera-ready/code_clippy_logo.jpg" width="256"/>
    <br>
    Courtesy of the awesome Aimee Trevett!
<p>

This extension is an effort to create an open source version of [Github Copilot](https://copilot.github.com/) where both the extension, model, and data that the model was trained on is free for everyone to use. If you'd like to learn more about how the model power Code Clippy, check out this [repo](https://github.com/ncoop57/gpt-code-clippy/).

This extension also sits completely atop this other clone of Github Copilot aptly named [Captain Stack](https://github.com/hieunc229/copilot-clone), since instead of synthesizing the answers using deep learning, it extracts them from StackOverflow posts.

## Demo

<p align="center">
    <br>
    <img src="code-clippy-demo.gif" width="80%"/>
    </br>
<p>

## Table of contents:

1. [How to Install](#1-installation)
2. [Using Code Clippy](#2-play-with-captain-stack)
3. [Limitations](#3-limitations)

---

## 1. How to Install

In order to use the extension, you will need to download and install [VSCode Insider](https://code.visualstudio.com/insiders/) and [Node and npm](https://nodejs.dev/learn/how-to-install-nodejs) (tested on Node `10.19.0` and npm `7.13.0`). Additionally, you will need a [Huggingface account](https://huggingface.co/join) in order to obtain the necessary API key that is used to authorize calls to Huggingface's Inference API.

Download and install Code Clippy:
```bash
git clone https://github.com/CodedotAl/code-clippy-vscode
cd code-clippy-vscode
npm install
code-insiders .
```

---

## 2. Using Code Clippy

Once VSCode Insider has opened up, you can press F5 to launch the extension in another VSCode window in debug model that you can test out. Open up a file of your choice in the new VSCode window and start typing. You will be prompted to enter an API key, go to your Huggingface account's [API token page](https://api-inference.huggingface.co/dashboard/api_token) and copy your API key and paste it into the prompt. Now you should be able to type and see suggestions! To accept a suggestion, just press tab and to cycle through different suggestions press `ALT + [` to go to the next suggestion or `ALT + ]` to go to the previous one.

**Note -**

It can take a few seconds (~20seconds) to spin up the model on Huggingface's servers, so if you get an error about waiting for the model to load, just give it about 20 seconds and try again. If you don't see any suggestions, make sure that `showInlineCompletions` is enabled in your settings:
```
"editor.inlineSuggest.enabled": true
```

Additionally, Huggingface's Inference API free tier has a limited amount of requests you can make per hour and per month so if you are on the free tier you will only be able to use the extension as a demo. If you would like to be able to use the extension without this limitation you can host the model yourself and edit the code to send requests there or you can upgrade your Huggingface account to a different [tier](https://huggingface.co/pricing).

You can also edit the model used to generate the code suggestions. I recommend using EleutherAI/gpt-neo-1.3B or EleutherAI/gpt-neo-2.7B over the default as in my testing they produce a lot better suggestions, but is significantly slower. To edit the model press `CTRL + SHIFT + P` to bring up the command prompt and type settings and select "Preferences: Open User Settings". This will open another tap with your settings. Search for "code clippy" and update the "Hf Model Name" configuration to be whatever model you want such as:
```
EleutherAI/gpt-neo-1.3B
```

From these code clippy settings, you can also update your API key or enable using GPU for doing the generation. However, for this feature to work, you need to have at least the Startup tier for Huggingface's Inference API.

---

## 3. Limitations

| :exclamation:  **Important -**  First and formost, this extension is a **prototype** and the model it was trained on is for **research purposes** only and should not be used for developing real world applications. This is because the default model that is used to generate the code suggestions was trained on a large set of data scraped from [GitHub]() that might have contained things such as vulnerable code or private information such as private keys or passwords. Vulnerable code or private information can and therefore probably will leak into the suggestions. Currently the suggestions are just limited to a few additional tokens since the model starts to [hallucinate]() variables and methods the longer suggestions it is allowed to generate. If you would like to read more about the shortcomings of the model used in the generation and data used to train the model please refer to this [model card]() and [datasheet]() that explain it more in-depth. If you would like to learn more about how the model was trained and data was collected please refer to this [repository](https://github.com/ncoop57/gpt-code-clippy/). |
|-----------------------------------------|
