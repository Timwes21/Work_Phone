test_string = "Called=%2B17722476154&ToState=FL&DialCallStatus=no-answer&CallerCountry=US&Direction=inbound&CallerState=FL&ToZip=&DialCallSid=CA78ac2c94403f1c4bd6088a9f2c4fe6b5&CallSid=CA4b2c80691a3b7059f44c09530901f525&To=%2B17722476154&CallerZip=&ToCountry=US&CalledZip=&ApiVersion=2010-04-01&CalledCity=&CallStatus=in-progress&From=%2B17722065315&DialBridged=false&AccountSid=ACb350721dafbd9acf0ea86dff255d11e0&CalledCountry=US&CallerCity=&ToCity=&FromCountry=US&Caller=%2B17722065315&FromCity=&CalledState=FL&FromZip=&FromState=FL"
key = "DialCallCallStatus="
res = test_string.split("&")
body = {i.split("=")[0]: i.split("=")[1] for i in test_string.split("&")}




