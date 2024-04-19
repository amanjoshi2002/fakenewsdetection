# import 'package:flutter/material.dart';
# import 'package:flutter/services.dart';
# import 'package:clipboard/clipboard.dart';
# import 'dart:async';

# void main() {
#   runApp(MyApp());
# }

# class MyApp extends StatelessWidget {
#   @override
#   Widget build(BuildContext context) {
#     return MaterialApp(
#       debugShowCheckedModeBanner: false,
#       home: FrontPage(),
#     );
#   }
# }

# class FrontPage extends StatelessWidget {
#   @override
#   Widget build(BuildContext context) {
#     return Scaffold(
#       body: Stack(
#         children: [
#           Image.asset(
#             'assets/newsp.jpg',
#             fit: BoxFit.cover,
#             width: double.infinity,
#             height: double.infinity,
#           ),
#           Align(
#             alignment: Alignment.bottomCenter,
#             child: DraggableArrow(
#               onPressed: () {
#                 Navigator.push(
#                   context,
#                   MaterialPageRoute(builder: (context) => NewsPage()),
#                 );
#               },
#             ),
#           ),
#         ],
#       ),
#     );
#   }
# }

# class DraggableArrow extends StatefulWidget {
#   final Function()? onPressed;

#   const DraggableArrow({Key? key, this.onPressed}) : super(key: key);

#   @override
#   _DraggableArrowState createState() => _DraggableArrowState();
# }

# class _DraggableArrowState extends State<DraggableArrow> {
#   double _position = 0;

#   @override
#   Widget build(BuildContext context) {
#     return GestureDetector(
#       onVerticalDragUpdate: (details) {
#         setState(() {
#           _position += details.delta.dy;
#         });
#       },
#       onVerticalDragEnd: (details) {
#         if (_position < -50) {
#           Navigator.push(
#             context,
#             MaterialPageRoute(builder: (context) => NewsPage()),
#           );
#         }
#         setState(() {
#           _position = 0;
#         });
#       },
#       child: SizedBox(
#         height: MediaQuery.of(context).size.height / 4,
#         child: Container(
#           width: double.infinity,
#           decoration: BoxDecoration(
#             color: Colors.grey.shade300,
#             borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
#           ),
#           child: Column(
#             mainAxisAlignment: MainAxisAlignment.center,
#             children: [
#               Icon(Icons.arrow_upward),
#               SizedBox(height: 10),
#               ElevatedButton(
#                 onPressed: widget.onPressed,
#                 style: ElevatedButton.styleFrom(
#                   backgroundColor: Colors.green,
#                   padding: EdgeInsets.symmetric(vertical: 10, horizontal: 40),
#                   shape: RoundedRectangleBorder(
#                     borderRadius: BorderRadius.circular(20),
#                   ),
#                 ),
#                 child: Text(
#                   'Go',
#                   style: TextStyle(fontSize: 20),
#                 ),
#               ),
#               SizedBox(height: 10),
#               Row(
#                 mainAxisAlignment: MainAxisAlignment.center,
#                 children: [
#                   Container(
#                     width: 60,
#                     height: 60,
#                     decoration: BoxDecoration(
#                       color: Colors.grey.shade300,
#                       shape: BoxShape.circle,
#                     ),
#                     child: Image.asset('assets/logo.png'),
#                   ),
#                   SizedBox(width: 8),
#                   Text(
#                     'fakecheckmate',
#                     style: TextStyle(
#                       fontSize: 14,
#                       color: Colors.blue,
#                       fontStyle: FontStyle.italic,
#                     ),
#                   ),
#                 ],
#               ),
#             ],
#           ),
#         ),
#       ),
#     );
#   }
# }

# class NewsPage extends StatefulWidget {
#   @override
#   _NewsPageState createState() => _NewsPageState();
# }

# class _NewsPageState extends State<NewsPage> {
#   late String _clipboardData;
#   late Timer _timer;

#   @override
#   void initState() {
#     super.initState();
#     _getClipboardData();
#     _timer = Timer.periodic(Duration(seconds: 1), (timer) {
#       _getClipboardData();
#     });
#   }

#   @override
#   void dispose() {
#     _timer.cancel();
#     super.dispose();
#   }

#   Future<void> _getClipboardData() async {
#     ClipboardData? clipboardData =
#         await Clipboard.getData(Clipboard.kTextPlain);
#     setState(() {
#       _clipboardData = clipboardData?.text ?? 'No clipboard data';
#     });
#   }

#   @override
#   Widget build(BuildContext context) {
#     return Scaffold(
#       appBar: AppBar(
#         title: Text('News'),
#         actions: [
#           IconButton(
#             onPressed: () {
#               // Handle settings icon tap
#             },
#             icon: Icon(Icons.settings),
#           ),
#         ],
#       ),
#       body: Padding(
#         padding: EdgeInsets.all(20),
#         child: Column(
#           crossAxisAlignment: CrossAxisAlignment.stretch,
#           children: [
#             SizedBox(height: 20),
#             SizedBox(height: 20),
#             Container(
#               padding: EdgeInsets.all(20),
#               decoration: BoxDecoration(
#                 borderRadius: BorderRadius.circular(20),
#                 color: Colors.blue,
#               ),
#               child: Text(
#                 _clipboardData,
#                 style: TextStyle(fontSize: 18, color: Colors.white),
#               ),
#             ),
#             SizedBox(height: 20),
#             Container(
#               padding: EdgeInsets.all(20),
#               decoration: BoxDecoration(
#                 borderRadius: BorderRadius.circular(20),
#                 color: Colors.orange,
#               ),
#               child: Text(
#                 'Answer',
#                 style: TextStyle(fontSize: 18, color: Colors.white),
#               ),
#             ),
#             SizedBox(height: 20),
#             Row(
#               mainAxisAlignment: MainAxisAlignment.center,
#               children: [
#                 CustomButton(
#                   name: 'Add Manual',
#                   color: Colors.purple,
#                   icon: Icons.library_add,
#                   onPressed: () {
#                     Navigator.push(
#                       context,
#                       MaterialPageRoute(builder: (context) => ManualEntryPage()),
#                     );
#                   },
#                 ),
#                 SizedBox(width: 10),
#                 CustomButton(
#                   name: 'Report',
#                   color: Colors.deepOrange,
#                   icon: Icons.report,
#                   onPressed: () {
#                     Navigator.push(
#                       context,
#                       MaterialPageRoute(builder: (context) => ReportPage()),
#                     );
#                   },
#                 ),
#               ],
#             ),
#           ],
#         ),
#       ),
#     );
#   }
# }

# class CustomButton extends StatelessWidget {
#   final String name;
#   final Color color;
#   final IconData icon;
#   final Function()? onPressed;

#   CustomButton({
#     required this.name,
#     required this.color,
#     required this.icon,
#     this.onPressed,
#   });

#   @override
#   Widget build(BuildContext context) {
#     return TextButton(
#       onPressed: onPressed,
#       style: TextButton.styleFrom(
#         foregroundColor: Colors.white,
#         padding: EdgeInsets.symmetric(vertical: 15, horizontal: 20),
#         backgroundColor: color,
#         shape: RoundedRectangleBorder(
#           borderRadius: BorderRadius.circular(20),
#         ),
#       ),
#       child: Row(
#         mainAxisSize: MainAxisSize.min,
#         children: [
#           Icon(icon),
#           SizedBox(width: 10),
#           Text(
#             name,
#             style: TextStyle(fontSize: 18),
#           ),
#         ],
#       ),
#     );
#   }
# }

# class ManualEntryPage extends StatelessWidget {
#   @override
#   Widget build(BuildContext context) {
#     return Scaffold(
#       appBar: AppBar(
#         title: Text('Manual Entry'),
#       ),
#       body: Center(
#         child: Column(
#           mainAxisAlignment: MainAxisAlignment.center,
#           children: [
#             Text(
#               'Result',
#               style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
#             ),
#             SizedBox(height: 20),
#             Padding(
#               padding: const EdgeInsets.symmetric(horizontal: 40),
#               child: TextField(
#                 decoration: InputDecoration(
#                   hintText: 'Enter your input',
#                   border: OutlineInputBorder(),
#                 ),
#               ),
#             ),
#             SizedBox(height: 20),
#             ElevatedButton(
#               onPressed: () {
#                 // Add your submit logic here
#               },
#               child: Text('Submit'),
#             ),
#           ],
#         ),
#       ),
#     );
#   }
# }

# class ReportPage extends StatelessWidget {
#   @override
#   Widget build(BuildContext context) {
#     return Scaffold(
#       appBar: AppBar(
#         title: Text('Report Issue'),
#       ),
#       body: Padding(
#         padding: const EdgeInsets.all(20.0),
#         child: Column(
#           mainAxisAlignment: MainAxisAlignment.center,
#           children: [
#             TextField(
#               decoration: InputDecoration(
#                 hintText: 'Enter your report here',
#               ),
#               maxLines: 5,
#             ),
#             SizedBox(height: 20),
#             ElevatedButton(
#               onPressed: () {
#                 // Implement submit functionality here
#               },
#               child: Text('Submit'),
#             ),
#           ],
#         ),
#       ),
#     );
#   }
# }
