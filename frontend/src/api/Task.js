import api from "@/api/axios.js";

class Task{
  getAll(group, user, completed) {
    return api.get(`tasks?group=${group}`)
  }

  createTask(data){
    return api.post('tasks/', data)
  }

  updateTask(data, id){
    return api.patch(`tasks/${id}`, data)
  }

  deleteTask(id){
    return api.delete(`tasks/${id}`)
  }
}

export default new Task()
