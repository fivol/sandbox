const axios = require('axios');

const apikey = '4a3fd1b3-a363-4a00-b0a9-e89198dd009d'

let schedule = undefined

const FightsTimeTable = {

    url: `https://api.rasp.yandex.net/v3.0/schedule/?apikey=${apikey}&station=svo&transport_types=plane&system=iata`,

    getSchedule: () => {
        // Получение расписания

        if (schedule !== undefined) {
            return schedule;
        }
        return axios.get(this.url).then(response => {
            return response.data
        })
    },
    exploreFlight: (code) => {
        return this.getSchedule().then(
            data => {
                const flights = data['schedule'].filter(item => item['thread']['number'] === code)
                if (flights.length === 0) {
                    return undefined;
                }
            }
        )
    },
    getFlightsByTime: (time) => {
        // time is string like "00:12"
        return this.getSchedule().then(data => {
            return data['schedule'].filter(item => item['departure'] === time)
        });
    },
    getFlightsByCity: (cityName) => {
        // "Нью-Йорк"
        return this.getSchedule().then(data => {
            return data['schedule'].filter(item => item['thread']['title'].toLowerCase().includes(cityName))
        });
    }
}


// exploreFlight('SU 1736').then(
//     result => {
//         console.log(result)
//     }
// )
