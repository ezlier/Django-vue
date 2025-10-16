<template>
    <div class="content">
        <div class="row">
            <div class="leftcolumn">

            </div>
            
            <div class="rightcolumn">

            </div>
        </div>

    </div>
</template>

<style scoped>
.content{
    height: 1800px;
    background-color: rgba(204, 204, 204, 0.9);
}

.row {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    max-width: 1280px;
    padding: 10px;
    justify-content: center;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

.leftcolumn {
  flex: 0 0 20%; /* 固定25%宽度 */
  /* background-color: #f1f1f1; */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 1px 2px 5px #fcbad3;
  background-color: wheat;
}

.rightcolumn {
  flex: 1;       
  padding: 20px;
  min-width: 0; 
  width: 100%;
  border-radius: 8px;
  /* box-shadow: 2px 2px 5px #000; */
}
</style>