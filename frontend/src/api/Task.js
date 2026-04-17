import api from "@/api/axios.js";

class Task{
  getAllTasks(){
    return api.get('tasks/')
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
