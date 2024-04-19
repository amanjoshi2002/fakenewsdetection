import 'package:flutter/material.dart';
import 'package:dash_bubble/dash_bubble.dart';
import 'package:flutter/services.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Icon Overlay Demo',
      home: const IconOverlayDemo(),
    );
  }
}

class IconOverlayDemo extends StatefulWidget {
  const IconOverlayDemo({Key? key}) : super(key: key);

  @override
  _IconOverlayDemoState createState() => _IconOverlayDemoState();
}

class _IconOverlayDemoState extends State<IconOverlayDemo> {
  String _currentIcon = 'lens'; // Initial icon
  static const String trueIcon = 'trueicon'; // True icon
  static const String falseIcon = 'falseicon'; // False icon
  bool _bubbleShown = false;

  Future<void> _startIconOverlay(BuildContext context) async {
    print('Starting icon overlay with current icon: $_currentIcon');
    if (_bubbleShown) {
      await DashBubble.instance.stopBubble();
    }
    await DashBubble.instance.startBubble(
      bubbleOptions: BubbleOptions(
        bubbleIcon: _currentIcon, // Use the current icon
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
        print('Icon tapped: $_currentIcon');
        setState(() {
          _currentIcon = _currentIcon == trueIcon ? falseIcon : trueIcon;
          print('Changed icon to: $_currentIcon');
        });
        _startIconOverlay(context);
      },
    );
    _bubbleShown = true;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Icon Overlay Demo'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            await _startIconOverlay(context);
          },
          child: const Text('Start Overlay'),
        ),
      ),
    );
  }
}