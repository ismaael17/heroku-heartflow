import axios from 'axios';

const API_URL = 'https://heartflow-support-system.herokuapp.com/'

class AuthService {

    async getInfo(token) {
        return await axios.get(API_URL + 'get-info', {headers: {
            Authorization: ('Token ' + token)
        }})
    }

    getBranches() {
        return axios.get(API_URL + "branch"
        ).then(response => {
            return response
        })
    }

    async getVolunteerDetails(token, id) {
        return await axios.get(API_URL + 'get-info/' + id, {
            headers: {
                Authorization: ('Token ' + token)
            }
        })
    }

    async getPendingVolunteers(token, status) {
        return await axios.get(API_URL + 'pending-volunteers/' + status,  {headers: {
            Authorization: ('Token ' + token)
        }}).then(response => {
            console.log(response)
            return response
        })
    }

    async changeStatus(token, id, status, date) {
        console.log(date)
        var postData = {
            id: id,
            date: date
          };

        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return await axios.patch(API_URL + 'pending-volunteers/' + status + '/', postData, {
            headers : axiosConfig
        }).then(response => {
            console.log(response)
        })
    }

    volunteerSignup(first_name, last_name, email, phone, branch, reason) {
        return axios.post(API_URL + 'volunteers', {
            first_name,
            last_name,
            email,
            branch,
            phone,
            reason
        })
    }

    setPassword(password, token) {
        return axios.post(API_URL + 'reset-password/' + token, {
            password
        }).then(response => {
            console.log(response)
        })
        .catch((error) => {
            console.log("setPassword", error);
          });  
    }

    async userType(token) {
        return await axios.get(API_URL + 'user-type', {headers: {
                Authorization: ('Token ' + token)
            }
        })
    }
    

    async login(username, password) {
        return await axios.post(API_URL + 'login', {
            username,
            password
        }).then(response => {
            console.log(response)
            console.log(response.data.token)
            return response
        })
    }
}
export default new AuthService();


