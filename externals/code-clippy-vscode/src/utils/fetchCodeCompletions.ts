import fetch from "node-fetch";

export type FetchCodeCompletions = {
    completions: Array<string>
}

export function fetchCodeCompletionTexts(prompt: string, fileName: string, MODEL_NAME: string, API_KEY: string, USE_GPU: boolean): Promise<FetchCodeCompletions> {
    console.log(MODEL_NAME)
    const API_URL = `https://api-inference.huggingface.co/models/${MODEL_NAME}`;
    // Setup header with API key
    // eslint-disable-next-line @typescript-eslint/naming-convention
    const headers = { "Authorization": `Bearer ${API_KEY}` };
    return new Promise((resolve, reject) => {
        // Send post request to inference API
        return fetch(API_URL, {
            method: "post",
            body: JSON.stringify({
                "inputs": prompt, "parameters": {
                    "max_new_tokens": 16, "return_full_text": false,
                    "do_sample": true, "temperature": 0.8, "top_p": 0.95,
                    "max_time": 10.0, "num_return_sequences": 3,
                    "use_gpu": USE_GPU
                }
            }),
            headers: headers
        })
        .then(res => res.json())
        .then(json => {
            if (Array.isArray(json)) {
                const completions = Array<string>()
                for (let i=0; i < json.length; i++) {
                    const completion =  json[i].generated_text.trimStart()
                    if (completion.trim() === "") continue

                    completions.push(
                        completion
                    )
                }
                console.log(completions)
                resolve({ completions })
            }
            else {
                console.log(json);
                throw new Error(json["error"])
            }
        })
        .catch(err => reject(err))
    })
}