# The Kobiton plugin for XebiaLabs XL Release product

This XL release Kobiton plugin allows XL Release to interact with [Kobiton](https://portal.kobiton.com) such as getting devices list, executing automation test, collecting execution result.

# Table of content
* [Feature task](#feature-task)
* [Set up with Kobiton Server](#Set-up-with-Kobiton-server)
    * [A. Preparation](#A.-Preparation)
        * [1. Getting Kobiton Username and API key ](#1.-Getting-Kobiton-Username-and-API-key)
        * [2. Getting SSH key for private repository](#2.-Getting-SSH-key-for-private-repository)
    * [B. Configuration](#B.-Configuration)
* [Set up release/phrase for Kobiton](#Set-up-release/phrase-for-Kobiton)
    * [A. General](#A.-General)
    * [B. Task](#B.-Task)
        * [1. List Available Devices](#1.-List-Available-Devices)
        * [2. Request Execute Test](#2.-Request-Execute-Test)
        * [3. Wait for Execution](#3.-Wait-for-Execution)
* [Start release/phrase](#Start-release/phrase)
* [Results from tasks](#Results-from-tasks)
___
## Feature task
- List available devices
- Request execute test
- Wait for execute (Collect result from test)
___
## Set up with Kobiton server
### A. Preparation
#### 1. Getting Kobiton Username and API key
Kobiton Username and API key are required for authenticating with Kobiton API.

> If you don't have a Kobiton account, visit https://portal.kobiton.com/register to create one.

To get your Kobiton Username and API Key, follow instructions at `IV. Configure Test Script for Kobiton` section on [our blog](https://kobiton.com/blog/tutorial/parallel-testing-selenium-webdriver/)

#### 2. Getting SSH key for private repository 
For executing automated test, Kobiton plugin supports test script stored on a Github repository. Therefore, this requires a SSH key for authenticating with your private repository on Github.

> If you haven't had SSH key yet, please visit follow [Github SSH key instruction](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) to create one.

> Note: for security, Kobiton plugin are not support passphrase for SSH key. Please, notice this when you generate SSH key.
___
### B. Configuration

1. In the XL Release home page, go to __Settings > Shared configuration > Kobiton: Server >__    ![](./readme/button1.png)

<img src="./readme/step2.png" alt="step2" width="600">

2. These are some information you need to fill in
    |Section|Description|
    | -----------------| --------------- |
    | Title            | Enter the name of your Kobiton Server |
    | Kobiton Username | Enter your Kobiton username |
    | Kobiton Api Key  | Enter Api key of your Kobiton account |
    | Kobiton Api Url  | Enter the url of Kobiton Api: `https://api.kobiton.com` |
    | Executor Server Url | Enter the url connect to Executor Server: `https://executor.kobiton.com` |

<img src="./readme/step3.png" alt="step3" width="600">

When all fills are filled as above, you can test the connection with Kobiton Server by pressing button ![button2](./readme/button2.png).

3. Only if it notices `Kobiton Server is available` as below, that means all your information is correct and XL Release is available to connect with Kobiton. Pleas press **Save** to apply. 

    <img src="./readme/serverconnected.png" alt="serverconnected" width="300">

> Note: when an error is shown that cannot connect to Api or Executor server, please make sure your information is correct and you are availble to access internet. If you make everything right but cannot access to Kobiton Server, contact us for more detail.
___
## Set up release/phrase for Kobiton

### A. General 

* From home page choose __> Release__. If you haven't had a release yet, choose __> New release__ to create one. 

<img src="./readme/release.png" alt="release" width="600"/>

* When a release is created, a new phrase shown on. Choose __> Add task > Manual > Kobiton > Choose task you want to start__
    
    <img src="./readme/addtask.png" alt="addtask" width="300"/>

### B. Task
Kobiton Plugin now supports 3 tasks on XL Release enviroment:

#### 1. List Available Devices
This task is used to get a list of available(online) devices on Kobiton environment. You can custom the task to have a specific devices-list as your requirements.

<img src="./readme/listdevices1.png" alt="listdevices1" width="600">

* Input properties:

    | Field | Required | Type | Description |
    | ----- | -------- | ---- |----------- |
    |Favorite/In-house/Cloud Devices| Yes | Tick box | The group containing devices that you want to use for automation test. Note: you must choose at least 1 of these 3 options. |
    |Android/iOS Devices| Yes | Tick box | Mobile device OS that you want to get list. Note: you must choose at least 1 of these 2 options. |
    | Group Id | No | String | The ID of a specific group you want to get devices from. Default, it will be "Default Group". For GroupID information, you can visit [Kobiton group setting](https://docs.kobiton.com//organization-management/automation-for-groups/default-group-setting/). |
    
* Custom Params: Kobiton Api supports to get devices list with some specific properties such as device name, device model, device udid, etc. 
    > Vist our [Api Document](https://api.kobiton.com/docs/#get-all-devices) to have information about the parameters we support. 

    * Adding a custom parameter:

    | Step | Image | 
    | ---- | ----- |
    | Visit Api document above to get the right parameter's name | <img src="./readme/apiGetDevices.png" alt="apiGetDevices" width="400"> |
    | Input the parameter name in `Key` and its value | <img src="./readme/customparams0.png" alt="customparams0" width="400"> |
    | Press `Add` to apply this properties |  <img src="./readme/customparams1.png" alt="customparams1" width="400"> |
    | Result | <img src="./readme/customparams2.png" alt="customparams2" width="400"> |

* Output Properties: If you want to use the output from this task to the next task, you need to create a variable to save the list of devices.

    > Note: please choose some specific devices by using custom params. Because the next task will pick all devices in this output to execute test one by one. 

    | Step | Image | 
    | ---- | ----- |
    | Type in textbox the variable's name you want to save | <img src="./readme/outputlist0.png" alt="outputlist0" width="400"> |
    | Click at the row below `${} Create a new varaible of type key-value map` to create varaible |  <img src="./readme/outputlist1.png" alt="outputlist1" width="400"> |
    | Result | <img src="./readme/outputlist2.png" alt="outputlist2" width="400"> |

When properties are filled, update your task's information as your need: start date, due date, assignees, watchers, etc. 

Finally, you just close the task window, it will autosave. 
 
#### 2. Request Execute Test
This is the task used for Automated test execution. 

<img src="./readme/execute.png" alt="execute" width="600">

* List available devices: place the output of task 1 (if exist) to this section.

    |Step|Description|
    |----|----|
    |Click the button ![button3](./readme/button3.png)| <img src="./readme/task2param1.png" alt="task2param1" width="400"> |
    |Input exactly variable you created in task 1 in the textbox |  <img src="./readme/task2param1b.png" alt="task2param1b" width="400"> |
    |Result|<img src="./readme/task2param1c.png" alt="task2param1c" width="400">|

* Input properties
    | Field | Required | Type | Description |
    | ----- | -------- | ---- |----------- |
    |In-house devices udid|No|String|The udid of your private host devices on Kobiton Desktop. Visit our [document](https://docs.kobiton.com/device-lab-management/kobiton-desktop-app/getting-started-desktop-app/) for more detail about self host devices. |
    |Capture Screenshots|No|Tickbox|Screenshots will be stored on our session detail of [portal](https://portal.kobiton.com/sessions) if you select this section. |
    |Orientation|Yes|Selection|Start app as landscape or portrait.|
    |Test execution type|Yes|Selection|Execute an automation test on app or browser|
    |Browser|No|Selection|Type of browser: Chrome (android) or Safari (iOs). Required if you chose to test on browser.|
    |App URL/App ID|Yes|String|Your app's public URL or Kobiton App ID. Required if you chose to test on apps.|
    |Group ID|No|String|The ID of a specific group you want to get devices from. Default, it will be "Default Group". For GroupID information, you can visit [Kobiton group setting](https://docs.kobiton.com//organization-management/automation-for-groups/default-group-setting/).|
    |Git repository|Yes|String|URL to your Git repository that contains automation test scripts.|
    |Execute branch|No|String|Select the branch contain your script because you cannot switch branch after cloning. Default branch is master.|
    |Private repository SSH Key|Yes|String|Copy whole of file of your private SSH key and paste to this section.|
    |Commands|Yes|Yaml syntax|Input commands needed to execute your test script.|

    Example: 

    <img src="./readme/exampleExecute.png" alt="exampleExecute" width="600">

* Output properties: You will need to store output in a variable
for the use of task 3. 

    | Step | Image | 
    | ---- | ----- |
    | Type in textbox the variable's name you want to save | <img src="./readme/outputjob1.png" alt="outputjob1" width="400"> |
    | Click at the row below `${} Create a new varaible of type key-value map` to create varaible |  <img src="./readme/outputjob2.png" alt="outputjob2" width="400"> |
    | Result | <img src="./readme/outputjob3.png" alt="outputjob3" width="400"> |
    

#### 3. Wait for Execution
This task will collect the result from task 2 to let you know the automated test is pass or fail.

<img src="./readme/waitforexecute.png" alt="waitforexecute" width="600">

* Input properties
    | Field | Required | Type | Description |
    | ----- | -------- | ---- |----------- |
    |Job IDs |Yes|Sting| Input the output variable of task 2|
    |Terminate when failed|No|Tickbox|The release of XL will be terminated if at least 1 failed.| 

___ 
## Start release/phrase

When you finish editing your tasks and phrases, you can prress button **Start release** to start your release. 

<img src="./readme/startrelease.png" alt="startrelease" width="600">

___
## Results from tasks

Here are some example success output of each task:

#### 1. List Available Devices
A list of available devices will be shown here with the Key is device's udid and values are device information. If there is no device  in output, that means there is no available devices match your params at the moment. In that case, please try again later or pick another devices. 

<img src="./readme/outputlist.png" alt="startroutputlistelease" width="600">

#### 2. Request Execute Test
The output is the job id, which is used in task 3. If there is nothing in the output, please check if devices-list exists or not. Moreover, you can download the task's log in the attachment section in order to get detail information.

<img src="./readme/outputexecute.png" alt="outputexecute" width="600">

#### 3. Wait for Execution

After execution the test script, you will know if the test can be executed or not.

<img src="./readme/lastresult1.png" alt="lastresult1" width="600">

In case that the test is execute successfully, you can download the log of test report in the section **Comment**:

<img src="./readme/lastresult2.png" alt="lastresult2" width="600">
