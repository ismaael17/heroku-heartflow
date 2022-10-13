import axios from "axios";
import {config} from "process";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const API_URL = 'https://heartflow-support-system.herokuapp.com/'

class VolunteersService {
    getOnlineOrders(token, status) {
        return axios.get(API_URL + "coupons/" + status, {
            headers: {
            Authorization: ('Token ' + token)
        }}).then(response => {
            return response
        })
    }

    getDeliveries(token, paid) {
        let paidStatus = ""
        // eslint-disable-next-line default-case
        switch (paid) {
            case "All":
                paidStatus = "All"
                break
            case "Paid":
                paidStatus = "true"
                break
            case "Not Paid":
                paidStatus = "false"
                break
            default:
                paidStatus = "Director"
        }


        return axios.get(API_URL + "delivery/" + paidStatus, {
            headers: {
                Authorization: ('Token ' + token)
            }}).then(response => {
            return response
        })
    }

    async pickupCoupons(token, amount, source, serial_letter, range_from, range_to) {

        const postData = {
            amount: amount,
            source: source,
            serial_letter: serial_letter,
            range_from: range_from,
            range_to: range_to
        };

        const axiosConfig = {
            'Authorization': 'Token ' + token
        };

        return await axios.post(API_URL + 'picked-up', postData, {
            headers: axiosConfig
        }).then(response => {
            return(response)
        })
    }

    async discardCoupons(token, amount, reason, serial_letter, range_from, range_to) {
        const postData = {
            amount: amount,
            
            serial_letter: serial_letter,
            range_from: range_from,
            range_to: range_to,
            reason: reason
        };


        const axiosConfig = {
            'Authorization': 'Token ' + token
        };

        return await axios.post(API_URL + 'discard-coupons', postData, {
            headers: axiosConfig
        }).then(response => {
            return (response)
        })
    }

    async exchangeCoupons(token, amount, serial_letter, range_from, range_to, reason, volunteer) {
        let volunteerID = parseInt(volunteer)
        const postData = {
            amount: amount,
            serial_letter: serial_letter,
            range_from: range_from,
            range_to: range_to,
            reason: reason,
            to_volunteer :volunteerID
        };

        const axiosConfig = {
            'Authorization': 'Token ' + token
        };

        return await axios.post(API_URL + 'exchange-coupons', postData, {
            headers: axiosConfig
        }).then(response => {
            console.log(response)
            return (response)
        })
    }

    async deliveredCoupons(token, amount, comment, serial_letter, range_from, range_to, outlet) {
        const postData = {
            amount: amount,
            comments: comment,
            serial_letter: serial_letter,
            range_from: range_from,
            range_to: range_to,
            company: outlet,
        };

        const axiosConfig = {
            'Authorization': 'Token ' + token
        };

        return await axios.post(API_URL + 'deliver', postData, {
            headers: axiosConfig
        }).then(response => {
            console.log(response)
            return (response)
        })
    }

    getOutlets(token) {
        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return axios.get(API_URL + "register-company", {
            headers:axiosConfig
        }).then(response => {
            return response
        })
    }

    getOutlet(token, id) {
        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return axios.get(API_URL + "register-company/" + id, {
            headers:axiosConfig
        }).then(response => {
            return response
        })
    }

    async registerOutlet(token, companyName, repName, email, phone, address, branch, payment, policy) {
        const postData = {
            companyName: companyName,
            repName: repName,
            repEmail: email,
            phone: phone,
            address: address,
            branch: branch,
            payment_method: payment,
            policy: policy
        };
        console.log(postData)

        const axiosConfig = {
            'Authorization': 'Token ' + token
        };

        return await axios.post(API_URL + 'register-company', postData, {
            headers: axiosConfig
        }).then(response => {
            console.log(response)
            return (response)
        })
    }

    async changeStatus(token, status, id) {
        const postData = {
            status: status
        };

        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return await axios.patch(API_URL + "coupon/id=" + id, postData, {
            headers:axiosConfig
            
        }).then(response => {
            return response
        })
    }

    async changePaid(token, paid, id) {
        let paidStatus = ""
        // eslint-disable-next-line default-case
        switch (paid) {
            case "Paid":
                paidStatus = "true"
                break
            case "Not Paid":
                paidStatus = "false"
                break
        }
        const postData = {
            paid: paidStatus
        };

        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return await axios.patch(API_URL + "update-delivery/id=" + id, postData, {
            headers:axiosConfig

        }).then(response => {
            return response
        })
    }

    getVolunteers(token) {
        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return axios.get(API_URL + "get-volunteers-exchange", {
            headers:axiosConfig
        }).then(response => {
            return response
        })
    }

    editVolunteerProfile(token, first_name, last_name, branch, phone) {
        const postData = {
            first_name: first_name,
            last_name: last_name,
            branch: branch,
            phone: phone
        };

        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return axios.patch(API_URL + "get-info", postData,{
            headers:axiosConfig
        }).then(response => {
            return response
        })
    }

     async editOutlet(token, companyName, repName, email, phone, address, branch, payment, policy, active, id) {
        const postData = {
            companyName: companyName,
            repName: repName,
            repEmail: email,
            phone: phone,
            address: address,
            branch: branch,
            payment_method: payment,
            policy: policy,
            active: active
        };

        const axiosConfig = {
            'Authorization': 'Token ' + token
        };

        return await axios.patch(API_URL + 'update-company/id=' + id, postData, {
            headers: axiosConfig
        }).then(response => {
            return (response)
        })
    }



    editDirectorProfile(token, first_name, last_name, phone) {
        const postData = {
            first_name: first_name,
            last_name: last_name,
            phone: phone
        };

        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return axios.patch(API_URL + "get-info", postData,{
            headers:axiosConfig
        }).then(response => {
            return response
        })
    }

    getSource(token) {
        const axiosConfig = {
                'Authorization': 'Token ' + token
        };

        return axios.get(API_URL + "source", {
            headers:axiosConfig
        }).then(response => {
            return response
        })
    }



    getOrderDetails(token, id) {
        return axios.get(API_URL + "coupon/id=" + id, {
            headers: {
                Authorization: ('Token ' + token)
            }
        }).then(response => {
            return response
        })
    }

    getDeliveryDetails(token, id) {
        return axios.get(API_URL + "delivery/id=" + id, {
            headers: {
                Authorization: ('Token ' + token)
            }
        }).then(response => {
            return response
        })
    }

    getVolunteerDetails(token) {
        return axios.get(API_URL+"get-info", {
            headers: {
                Authorization: ('Token ' + token)
            }
        }).then(response => {
                return response
        })
    }
}

export default new VolunteersService();
