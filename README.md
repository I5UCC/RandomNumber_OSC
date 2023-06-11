# RandomNumber_OSC

Just sending some random Numbers to over OSC, with a configurable Interval.

The config.json file contains a `Parameters` array that contains all of the parameters sent. You can add or remove as much as you need.

```
"Parameters": [
        {
            "Name": "Random1",
            "Type": "float",
            "Min": 0.0,
            "Max": 1.0,
            "Interval": 0.1
        },
        {
            "Name": "Random2",
            "Type": "int",
            "Min": 0,
            "Max": 255,
            "Interval": 0.1
        },
        {
            "Name": "Random3",
            "Type": "bool",
            "Interval": 0.1
        }
    ]
```

3 types you can choose: `float`, `int` and `bool`. The name determines the Parameters name and Min and Max the minimum and maximum values the random number should be generated from. Interval is per Parameter and in seconds.

Thats it, have fun with this if you need it lol.
