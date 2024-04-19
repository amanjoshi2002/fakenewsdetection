import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:clipboard/clipboard.dart';
import 'package:dash_bubble/dash_bubble.dart';
import 'dart:async';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: FrontPage(),
    );
  }
}

class FrontPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Image.asset(
            'assets/newsp.jpg',
            fit: BoxFit.cover,
            width: double.infinity,
            height: double.infinity,
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: DraggableArrow(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => NewsPage()),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class DraggableArrow extends StatefulWidget {
  final Function()? onPressed;

  const DraggableArrow({Key? key, this.onPressed}) : super(key: key);

  @override
  _DraggableArrowState createState() => _DraggableArrowState();
}

class _DraggableArrowState extends State<DraggableArrow> {
  double _position = 0;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onVerticalDragUpdate: (details) {
        setState(() {
          _position += details.delta.dy;
        });
      },
      onVerticalDragEnd: (details) {
        if (_position < -50) {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => NewsPage()),
          );
        }
        setState(() {
          _position = 0;
        });
      },
      child: SizedBox(
        height: MediaQuery.of(context).size.height / 4,
        child: Container(
          width: double.infinity,
          decoration: BoxDecoration(
            color: Colors.grey.shade300,
            borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.arrow_upward),
              SizedBox(height: 10),
              ElevatedButton(
                onPressed: widget.onPressed,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green,
                  padding: EdgeInsets.symmetric(vertical: 10, horizontal: 40),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
                child: Text(
                  'Go',
                  style: TextStyle(fontSize: 20),
                ),
              ),
              SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    width: 60,
                    height: 60,
                    decoration: BoxDecoration(
                      color: Colors.grey.shade300,
                      shape: BoxShape.circle,
                    ),
                    child: Image.asset('assets/logo.png'),
                  ),
                  SizedBox(width: 8),
                  Text(
                    'fakecheckmate',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.blue,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class NewsPage extends StatefulWidget {
  @override
  _NewsPageState createState() => _NewsPageState();
}

class _NewsPageState extends State<NewsPage> {
  String _currentIcon = 'search'; // Initial icon
  static const String trueIcon = 'yes'; // True icon
  static const String falseIcon = 'no'; // False icon
  bool _bubbleShown = false;

  Future<void> _startIconOverlay(BuildContext context) async {
    print('Starting icon overlay with current icon: $_currentIcon');
    if (_bubbleShown) {
      await DashBubble.instance.stopBubble();
    }

    // Get clipboard data
    ClipboardData? clipboardData = await Clipboard.getData(Clipboard.kTextPlain);
    String userinput = clipboardData?.text ?? '';

    // Make HTTP request to send clipboard text to backend
    int response = await fetchDataFromAPI(userinput);

    // Determine the icon based on the response
    String icon = response == 1 ? trueIcon : falseIcon;

    await DashBubble.instance.startBubble(
      bubbleOptions: BubbleOptions(
        bubbleIcon: icon, // Use the icon based on the response
        startLocationX: 0,
        startLocationY: 100,
        bubbleSize: 60,
        opacity: 1,
        enableClose: true,
        closeBehavior: CloseBehavior.following,
        distanceToClose: 100,
        enableAnimateToEdge: true,
        enableBottomShadow: true,
        keepAliveWhenAppExit: false,
      ),
      onTap: () {
        print('Icon tapped: $icon');
        setState(() {
          _currentIcon = _currentIcon == trueIcon ? falseIcon : trueIcon;
          print('Changed icon to: $_currentIcon');
        });
        _startIconOverlay(context);
      },
    );
    _bubbleShown = true;
  }

  Future<int> fetchDataFromAPI(String userinput) async {
  try {
    // Make an HTTP request to your API endpoint
    final response = await http.post(
      Uri.parse('http://10.0.2.2:5000/detection'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8', // Set content type header
      },
      body: jsonEncode(<String, String>{
        'userinput': userinput,
      }),
    );

    print('API Response Status Code: ${response.statusCode}');
    print('API Response Body: ${response.body}');

    if (response.statusCode == 200) {
      // Parse the response and extract the prediction value
      final Map<String, dynamic> data = json.decode(response.body);
      final double prediction = double.parse(data['prediction']);
      return prediction.toInt(); // Convert prediction to integer
    } else {
      // Handle errors
      print('Failed to load data from API: ${response.reasonPhrase}');
      return 0; // Return 0 if there's an error
    }
  } catch (e) {
    // Handle exceptions
    print('Error fetching data from API: $e');
    return 0; // Return 0 if there's an exception
  }
}


  late String _clipboardData;
  late Timer _timer;
  bool isBubbleShown = false;

  @override
  void initState() {
    super.initState();
    _getClipboardData();
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      _getClipboardData();
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  Future<void> _getClipboardData() async {
    ClipboardData? clipboardData = await Clipboard.getData(Clipboard.kTextPlain);
    setState(() {
      _clipboardData = clipboardData?.text ?? 'No clipboard data';
    });
  }

  void _stopBubble() {
    if (isBubbleShown) {
      DashBubble.instance.stopBubble(); // Your logic to stop the bubble
      setState(() {
        isBubbleShown = false;
      });
    }
  }

/*
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/spectrathon/Team_PCCE
git push -u origin main
*/
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('News'),
        actions: [
          IconButton(
            onPressed: () {
              // Handle settings icon tap
            },
            icon: Icon(Icons.settings),
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () async {
                    await _startIconOverlay(context);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.black,
                    padding: EdgeInsets.symmetric(vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                  ),
                  child: Text(
                    'Start',
                    style: TextStyle(fontSize: 18, color: Colors.white),
                  ),
                ),
                ElevatedButton(
                  onPressed: _stopBubble,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.black,
                    padding: EdgeInsets.symmetric(vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                  ),
                  child: Text(
                    'Stop',
                    style: TextStyle(fontSize: 18, color: Colors.white),
                  ),
                ),
              ],
            ),
            SizedBox(height: 20),
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                color: Colors.black,
              ),
              child: Text(
                _clipboardData,
                style: TextStyle(fontSize: 18, color: Colors.white),
              ),
            ),
            SizedBox(height: 20),
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                color: Colors.black,
              ),
              child: Text(
                '---',
                style: TextStyle(fontSize: 18, color: Colors.white),
              ),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CustomButton(
                  name: 'Add Manual',
                  color: Colors.black,
                  icon: Icons.library_add,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => ManualEntryPage()),
                    );
                  },
                ),
                SizedBox(width: 10),
                CustomButton(
                  name: 'Report',
                  color: Colors.black,
                  icon: Icons.report,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => ReportPage()),
                    );
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class CustomButton extends StatelessWidget {
  final String name;
  final Color color;
  final IconData icon;
  final Function()? onPressed;

  CustomButton({
    required this.name,
    required this.color,
    required this.icon,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: onPressed,
      style: TextButton.styleFrom(
        foregroundColor: Colors.white,
        padding: EdgeInsets.symmetric(vertical: 15, horizontal: 20),
        backgroundColor: color,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon),
          SizedBox(width: 10),
          Text(
            name,
            style: TextStyle(fontSize: 18),
          ),
        ],
      ),
    );
  }
}

class ManualEntryPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Manual Entry'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Result',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40),
              child: TextField(
                decoration: InputDecoration(
                  hintText: 'Enter your input',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Add your submit logic here
              },
              child: Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}

class ReportPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Report Issue'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              decoration: InputDecoration(
                hintText: 'Enter your report here',
              ),
              maxLines: 5,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Implement submit functionality here
              },
              child: Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}