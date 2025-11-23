<template>
    <div class="comment-section">
        <div class="comment-input">
            <textarea class="form-control"></textarea>
            <div class="send">
                <span>
                    1 + 1 =
                    <input type="text" style="width: 40px;">
                </span>
                <button class="custom-btn btn-8" @click=""><span>这是提交喵</span></button>
            </div>
        </div>
        <div class="comment-list">
            <div class="comt-header">
                <span class="name">name</span>
                <span class="time">time</span>
            </div>
            <div class="comt-body">
                text
            </div>
        </div>
    </div>
</template>

<style scoped>
.comment-input {
    border: 2px solid #ccd4d9;
}

.send {
    text-align: right;
    width: 100px;
    height: 36px;
}

.form-control {
    resize: none;
    width: 100%;
    height: 68px;
    border: none;
    outline: none;
    background-image: url('@/assets/img/bg4.png');
    background-repeat: no-repeat;
    background-position: right bottom;
    background-size: 60px 60px;
    line-height: 22px;
    font-size: 14px;
}

/* 名字与时间 */
.comt-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.name {
    font-weight: 600;
    color: #7b4bb7;
    font-size: 1.1em;
}

.time {
    font-size: 0.85em;
    color: #888;
}

/* 正文部分自适应高度 */
.comt-body {
    white-space: pre-wrap;
    font-size: 1em;
    color: #333;
    padding: 0 0 15px;
}

.custom-btn {
    width: 100px;
    height: 100%;
    color: #fff;
    border-radius: 5px;
    padding: 10px 25px;
    font-family: 'Lato', sans-serif;
    font-weight: 500;
    background: transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    display: inline-block;
    box-shadow: inset 2px 2px 2px 0px rgba(255, 255, 255, .5),
        7px 7px 20px 0px rgba(0, 0, 0, .1),
        4px 4px 5px 0px rgba(0, 0, 0, .1);
    outline: none;
}

.btn-8 {
    background-color: #f0ecfc;
    background-image: linear-gradient(315deg, #f0ecfc 0%, #c797eb 74%);
    line-height: 42px;
    padding: 0;
    border: none;
}

.btn-8 span {
    position: relative;
    display: block;
    width: 100%;
    height: 100%;
}

.btn-8:before,
.btn-8:after {
    position: absolute;
    content: "";
    right: 0;
    bottom: 0;
    background: #c797eb;
    /*box-shadow:  4px 4px 6px 0 rgba(255,255,255,.5),
              -4px -4px 6px 0 rgba(116, 125, 136, .2), 
    inset -4px -4px 6px 0 rgba(255,255,255,.5),
    inset 4px 4px 6px 0 rgba(116, 125, 136, .3);*/
    transition: all 0.3s ease;
}

.btn-8:before {
    height: 0%;
    width: 2px;
}

.btn-8:after {
    width: 0%;
    height: 2px;
}

.btn-8:hover:before {
    height: 100%;
}

.btn-8:hover:after {
    width: 100%;
}

.btn-8:hover {
    background: transparent;
}

.btn-8 span:hover {
    color: #c797eb;
}

.btn-8 span:before,
.btn-8 span:after {
    position: absolute;
    content: "";
    left: 0;
    top: 0;
    background: #c797eb;
    box-shadow: 4px 4px 6px 0 rgba(255, 255, 255, .5),
        -4px -4px 6px 0 rgba(116, 125, 136, .2),
        inset -4px -4px 6px 0 rgba(255, 255, 255, .5),
        inset 4px 4px 6px 0 rgba(116, 125, 136, .3);
    transition: all 0.3s ease;
}

.btn-8 span:before {
    width: 2px;
    height: 0%;
}

.btn-8 span:after {
    height: 2px;
    width: 0%;
}

.btn-8 span:hover:before {
    height: 100%;
}

.btn-8 span:hover:after {
    width: 100%;
}
</style>