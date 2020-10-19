const login = require("facebook-chat-api");
const user_datas = require("./user_datas/datas.json")
const admin_data = require("./admin.json")
const fs = require("fs")
const dateFormat = require('dateformat');
var today=dateFormat(new Date(), "yyyy-mm-dd");
var PythonShell = require('python-shell');
// Create simple echo bot


login({email:admin_data.email, password: admin_data.password}, (err, api) => {
    if(err) return console.error(err);
    
    try{
        screenshot_directory = "screenshots/"+today
        fs.readdir(screenshot_directory, (error, filelist) => {
            filelist.forEach((e,i)=>{
                console.log(i)
                image_data = e.split("_")
                console.log(image_data)
                
                var facebook_uid = image_data[1].split(".")[0]
                var screenshot_path = __dirname +"/"+screenshot_directory +"/"+today+"_"+facebook_uid+".png"
                console.log("screenshot path : "+screenshot_path)
                console.log(facebook_uid)
                var msg = {
                    body: "success",
                    attachment: fs.createReadStream(screenshot_path) // TODO here!!
                }
                api.sendMessage(msg, facebook_uid);
                // api.sendMessage(msg,user_data)
            })
        })
    }catch(err){
        console.log(err)
    }
});
