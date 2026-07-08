<template>
    <button class="to-admin-btn">
        <a href="login" class="to-admin-btn__icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                <path fill="currentColor"
                    d="M288 320a224 224 0 1 0 448 0 224 224 0 1 0-448 0m544 608H160a32 32 0 0 1-32-32v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 0 1-32 32z">
                </path>
            </svg>
        </a>
    </button>
</template>

<style scoped>
.to-admin-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.04);
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s, transform 0.15s;
    overflow: hidden;
    position: relative;
    z-index: 10;
}

.to-admin-btn:hover {
    background: rgba(0, 0, 0, 0.08);
    transform: scale(1.08);
}

.dark .to-admin-btn {
    background: rgba(255, 255, 255, 0.06);
}

.dark .to-admin-btn:hover {
    background: rgba(255, 255, 255, 0.12);
}

.to-admin-btn__icon {
    line-height: 1;
    color: var(--ui-color);
    width: 24px;
    height: 24px;
}
</style>
