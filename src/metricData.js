
let data = {"metrics": [{"completion_percentage": 100, "metric_time": 24504, "start_time": 7904, "elapsed_time_in_milliseconds": 16600, "episode_status": "Lap complete", "crash_count": 0, "immobilized_count": 0, "off_track_count": 0, "reversed_count": 0, "reset_count": 0, "trial": 1}, {"completion_percentage": 100, "metric_time": 40632, "start_time": 24578, "elapsed_time_in_milliseconds": 16054, "episode_status": "Lap complete", "crash_count": 0, "immobilized_count": 0, "off_track_count": 0, "reversed_count": 0, "reset_count": 0, "trial": 2}, {"completion_percentage": 100, "metric_time": 61835, "start_time": 40705, "elapsed_time_in_milliseconds": 21130, "episode_status": "Lap complete", "crash_count": 0, "immobilized_count": 0, "off_track_count": 2, "reversed_count": 0, "reset_count": 2, "trial": 3}]}

 let interestedData = [];
 let completedTrainingNum = 0;
 let numberOfWithin15Sec = 0;
 let numberOfWithin16Sec = 0;
 let numberOfWithin17Sec = 0;
 let sumOfTotalTime = 0;

 for (let eachData of data.metrics) {
     //console.log(eachData)
     if (eachData.completion_percentage == 100) {
         interestedData.push(eachData)
         sumOfTotalTime+=eachData.elapsed_time_in_milliseconds;
         if (eachData.elapsed_time_in_milliseconds < 15000){
            numberOfWithin15Sec++;
         } else if (eachData.elapsed_time_in_milliseconds < 16000){
            numberOfWithin16Sec++;
         } else if (eachData.elapsed_time_in_milliseconds < 17000){
            numberOfWithin17Sec++;
         }
     }
 }
 
 interestedData.sort(function(a, b) {
     return a.elapsed_time_in_milliseconds - b.elapsed_time_in_milliseconds;
 });
 
 console.log(interestedData[0]);
 console.log('numberOfWithin15Sec: (14+): ' + numberOfWithin15Sec);
 console.log('numberOfWithin16Sec: (15+): ' + numberOfWithin16Sec);
 console.log('numberOfWithin17Sec: (16+): ' + numberOfWithin17Sec);
 console.log('totalNumberTraining: ' + data.metrics.length);
 console.log('totalNumberCompleted: ' + interestedData.length);
 console.log('Total average time: ' + sumOfTotalTime/interestedData.length);
 console.log('% of completed: ' + interestedData.length/data.metrics.length*100);
 console.log('% of 14+: ' + numberOfWithin15Sec/data.metrics.length*100);
 console.log('% of 15+: ' + numberOfWithin16Sec/data.metrics.length*100);
 console.log('% of 16+: ' + numberOfWithin17Sec/data.metrics.length*100);

