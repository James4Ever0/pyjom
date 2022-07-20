"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = void 0;
const vscode = require("vscode");
const config_1 = require("./config");
const fetchCodeCompletions_1 = require("./utils/fetchCodeCompletions");
function activate(context) {
    const disposable = vscode.commands.registerCommand('extension.code-clippy-settings', () => {
        vscode.window.showInformationMessage('Show settings');
    });
    context.subscriptions.push(disposable);
    const provider = {
        provideInlineCompletionItems: (document, position, context, token) => __awaiter(this, void 0, void 0, function* () {
            // Grab the api key from the extension's config
            const configuration = vscode.workspace.getConfiguration('', document.uri);
            const MODEL_NAME = configuration.get("conf.resource.hfModelName", "");
            const API_KEY = configuration.get("conf.resource.hfAPIKey", "");
            const USE_GPU = configuration.get("conf.resource.useGPU", false);
            vscode.comments.createCommentController;
            const textBeforeCursor = document.getText();
            if (textBeforeCursor.trim() === "") {
                return { items: [] };
            }
            const currLineBeforeCursor = document.getText(new vscode.Range(position.with(undefined, 0), position));
            // Check if user's state meets one of the trigger criteria
            if (config_1.default.SEARCH_PHARSE_END.includes(textBeforeCursor[textBeforeCursor.length - 1]) || currLineBeforeCursor.trim() === "") {
                let rs;
                try {
                    // Fetch the code completion based on the text in the user's document
                    rs = yield (0, fetchCodeCompletions_1.fetchCodeCompletionTexts)(textBeforeCursor, document.fileName, MODEL_NAME, API_KEY, USE_GPU);
                }
                catch (err) {
                    if (err instanceof Error) {
                        // Check if it is an issue with API token and if so prompt user to enter a correct one
                        if (err.toString() === "Error: Bearer token is invalid" || err.toString() === "Error: Authorization header is invalid, use 'Bearer API_TOKEN'") {
                            vscode.window.showInputBox({ "prompt": "Please enter your HF API key in order to use Code Clippy", "password": true }).then(apiKey => configuration.update("conf.resource.hfAPIKey", apiKey));
                        }
                        vscode.window.showErrorMessage(err.toString());
                    }
                    return { items: [] };
                }
                if (rs == null) {
                    return { items: [] };
                }
                // Add the generated code to the inline suggestion list
                const items = new Array();
                for (let i = 0; i < rs.completions.length; i++) {
                    items.push({
                        text: rs.completions[i],
                        range: new vscode.Range(position.translate(0, rs.completions.length), position),
                        trackingId: `snippet-${i}`,
                    });
                }
                return { items };
            }
            return { items: [] };
        }),
    };
    vscode.languages.registerInlineCompletionItemProvider({ pattern: "**" }, provider);
    // Be aware that the API around `getInlineCompletionItemController` will not be finalized as is!
    vscode.window.getInlineCompletionItemController(provider).onDidShowCompletionItem(e => {
        const id = e.completionItem.trackingId;
    });
}
exports.activate = activate;
