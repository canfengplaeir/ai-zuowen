<template>
  <dialog id="confirm_dialog" class="modal">
    <div class="modal-box">
      <h3 class="font-bold text-lg mb-4">{{ title }}</h3>
      <p>{{ message }}</p>
      <div class="modal-action">
        <button class="btn btn-error" @click="handleConfirm">确认</button>
        <button class="btn" @click="handleCancel">取消</button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>关闭</button>
    </form>
  </dialog>
</template>

<script>
import { ref } from 'vue'

let resolvePromise = null

export const useConfirm = () => {
  const showConfirm = (title, message) => {
    return new Promise((resolve) => {
      resolvePromise = resolve
      document.getElementById('confirm_dialog').showModal()
    })
  }
  return { showConfirm }
}

export default {
  name: 'ConfirmDialog',
  props: {
    title: {
      type: String,
      default: '确认'
    },
    message: {
      type: String,
      default: '确定要执行此操作吗？'
    }
  },
  setup() {
    const handleConfirm = () => {
      document.getElementById('confirm_dialog').close()
      resolvePromise?.(true)
    }

    const handleCancel = () => {
      document.getElementById('confirm_dialog').close()
      resolvePromise?.(false)
    }

    return {
      handleConfirm,
      handleCancel
    }
  }
}
</script> 