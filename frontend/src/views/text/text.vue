<template>
  <div class="bg"></div>
    <div class="card-container">
      <div class="card">
        <div class="card-header">
          <div class="card-tabs">
            <div class="card-tab active">Create an HTTP Server</div>
          </div>
        </div>
        <div class="card-body">
          <div class="line-numbers">
            <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span
            ><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span
            ><span>11</span><span>12</span><span>13</span><span>14</span>
          </div>
          <pre
            class="code-content"
          ><code><span class="code-comment">// server.mjs</span>
    <span class="code-keyword">import</span> { <span class="code-variable">createServer</span> } <span class="code-keyword">from</span> <span class="code-string">'node:http'</span>;

    <span class="code-keyword">const</span> <span class="code-variable-2">server</span> = <span class="code-function">createServer</span>((<span class="code-variable-2">req</span>, <span class="code-variable-2">res</span>) =&gt; {
      <span class="code-variable-2">res</span>.<span class="code-function">writeHead</span>(<span class="code-number">200</span>, { <span class="code-string">'Content-Type'</span>: <span class="code-string">'text/plain'</span> });
      <span class="code-variable-2">res</span>.<span class="code-function">end</span>(<span class="code-string">'Hello World!\n'</span>);
    });

    <span class="code-comment">// starts a simple http server locally on port 3000</span>
    <span class="code-variable-2">server</span>.<span class="code-function">listen</span>(<span class="code-number">3000</span>, <span class="code-string">'127.0.0.1'</span>, () =&gt; {
      <span class="code-function">console</span>.<span class="code-function">log</span>(<span class="code-string">'Listening on 127.0.0.1:3000'</span>);
    });

    <span class="code-comment">// run with `node server.mjs`</span>
    </code></pre>
        </div>
        <div class="card-footer">
          <span class="language-name">JavaScript</span>
          <button class="copy-button">
            <svg
              stroke="currentColor"
              fill="currentColor"
              stroke-width="0"
              viewBox="0 0 16 16"
              height="1em"
              width="1em"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H6zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1H2z"
              ></path>
            </svg>
            <span class="copy-button-text">Copy to clipboard</span>
          </button>
        </div>
      </div>
    </div>
    <Loading />
</template>

<script setup>
import "md-editor-v3/lib/style.css"
import Loading from "@/components/loading.vue"
</script>

<style scoped>
  .bg {
    position: fixed;
    /* 固定在视口 */
    top: 0;
    left: 0;
    width: 100vw;
    /* 拉伸占满全屏 */
    height: 100vh;
    background-image: url('@/assets/img/bg1.jpg');
    background-size: cover;
    /* 拉伸裁剪为最大，保持比例 */
    background-repeat: no-repeat;
    background-position: center;
    z-index: -1;
    /* 放到内容后面 */
  }

  .card-container {
    width: 380px;
    height: 300px;
    resize: both;
    overflow: hidden;
    background: #c0c0c0;
    border: 2px outset #c0c0c0;
    padding: 2px;
    font-family: "MS Sans Serif", "Tahoma", sans-serif;
    font-size: 11px;
  }

  .card {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background: #c0c0c0;
    border: 2px inset #c0c0c0;
    overflow: hidden;
    color: #000000;
  }

  .card-header {
    background: #000080;
    padding: 0;
    flex-shrink: 0;
    border-bottom: 1px solid #000000;
  }

  .card-tabs {
    display: flex;
    background: #c0c0c0;
    border-bottom: 1px solid #808080;
    height: 20px;
  }

  .card-tab {
    padding: 2px 8px;
    font-size: 11px;
    color: #000000;
    background: #c0c0c0;
    border: 2px outset #c0c0c0;
    border-bottom: none;
    cursor: pointer;
    height: 18px;
    margin-top: 1px;
  }

  .card-tab.active {
    background: #c0c0c0;
    border: 2px outset #c0c0c0;
    border-bottom: 1px solid #c0c0c0;
    margin-top: 0;
    height: 19px;
    position: relative;
    z-index: 2;
  }

  .card-body {
    display: flex;
    flex-grow: 1;
    overflow: auto;
    padding: 4px 0 4px 2px;
    font-family: "Courier New", monospace;
    font-size: 12px;
    line-height: 1.2;
    background: #ffffff;
    border: 1px inset #808080;
    margin: 2px;
  }

  .line-numbers {
    display: flex;
    flex-direction: column;
    padding: 0 6px;
    text-align: right;
    color: #808080;
    user-select: none;
    font-size: 12px;
    background: #f0f0f0;
    border-right: 1px solid #c0c0c0;
  }

  .code-content {
    margin: 0;
    padding: 0 4px;
    white-space: pre;
    overflow-x: auto;
    color: #000000;
  }

  .code-comment {
    color: #008000;
  }
  .code-keyword {
    color: #0000ff;
    font-weight: bold;
  }
  .code-variable {
    color: #800080;
  }
  .code-variable-2 {
    color: #ff0000;
  }
  .code-function {
    color: #000000;
    font-weight: bold;
  }
  .code-string {
    color: #808080;
  }
  .code-number {
    color: #000000;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #c0c0c0;
    padding: 2px 4px;
    border-top: 1px solid #808080;
    flex-shrink: 0;
    height: 22px;
  }

  .language-name {
    color: #000000;
    font-weight: normal;
  }

  .copy-button {
    display: flex;
    align-items: center;
    gap: 4px;
    background: #c0c0c0;
    color: #000000;
    border: 2px outset #c0c0c0;
    padding: 0 6px;
    cursor: pointer;
    font-size: 11px;
    height: 18px;
  }

  .copy-button:active {
    border: 2px inset #c0c0c0;
    padding: 1px 5px 0 7px;
  }

  .copy-button svg {
    width: 12px;
    height: 12px;
  }

  .copy-button-text {
    display: none;
  }

  .card-body::-webkit-scrollbar {
    width: 16px;
  }

  .card-body::-webkit-scrollbar-track {
    background: #c0c0c0;
    border: 1px outset #c0c0c0;
  }

  .card-body::-webkit-scrollbar-thumb {
    background: #c0c0c0;
    border: 2px outset #c0c0c0;
  }

  .card-body::-webkit-scrollbar-button {
    display: block;
    height: 16px;
    background: #c0c0c0;
    border: 2px outset #c0c0c0;
  }
</style>





