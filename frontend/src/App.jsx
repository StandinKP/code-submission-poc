import './App.css';
import 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-golang';
import 'ace-builds/src-noconflict/theme-github';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/theme-chaos';
import 'ace-builds/src-noconflict/theme-dracula';
import 'ace-builds/src-noconflict/ext-language_tools';
import 'ace-builds/src-noconflict/ext-themelist';

import AceEditor from 'react-ace';
import React from 'react';
import { useState } from 'react';

ace.config.set('basePath', 'node_modules/ace-builds/src-noconflict/');

function onLoad(editor) {
  console.log("i've loaded");
}

let pythonDefaultCode = `
def add(a, b):
  return a + b
print(add(3,8))
`;

const languages = ['python', 'javascript', 'java', 'go'];

function App() {
  const [mode, setMode] = useState(0);
  const [typedCode, setTypedCode] = useState(pythonDefaultCode);
  function onChange(newValue) {
    setTypedCode(newValue);
  }
  return (
    <div>
      <button
        onClick={(e) => {
          setMode(mode + 1);
          if (mode >= languages.length - 1) {
            setMode(0);
          }
        }}>
        Click Me
      </button>
      {languages[mode]}
      <AceEditor
        placeholder="Placeholder Text"
        mode={languages[mode]}
        theme="monokai"
        name="blah2"
        onLoad={onLoad}
        onChange={onChange}
        fontSize={16}
        showPrintMargin={true}
        showGutter={true}
        highlightActiveLine={true}
        value={typedCode}
        setOptions={{
          enableBasicAutocompletion: false,
          enableLiveAutocompletion: false,
          enableSnippets: false,
          showLineNumbers: true,
          tabSize: 2,
          animatedScroll: true,
        }}
      />
      <button
        type="button"
        onClick={async (e) => {
          e.preventDefault();
          const uri = `http://localhost:5000/accept`;
          const res = await fetch(uri, {
            method: 'POST',
            body: JSON.stringify({
              typed_code: typedCode,
              language: languages[mode],
            }),
            headers: {
              'Content-Type': 'application/json',
            },
          });
          const data = await res.json();
          console.log('Data>>>>>', data);
        }}>
        Submit
      </button>
    </div>
  );
}

export default App;
