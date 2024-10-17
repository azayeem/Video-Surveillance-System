import 'package:flutter/material.dart';
import 'package:fyp_app/login_page.dart';
import 'package:fyp_app/dashboard_page.dart';
import 'package:fyp_app/incidents_page.dart';
import 'package:fyp_app/signup_page.dart';
import 'package:fyp_app/forgot_password_page.dart';
import 'package:fyp_app/settings_page.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:intl/intl.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:url_launcher/url_launcher.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late IO.Socket socket;
  late FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin;
  int notificationId = 0;
  List<Map<String, String>> events = [];
  bool _isDarkMode = false; // Added dark mode state

  @override
  void initState() {
    super.initState();
    _initializeNotifications();
    _loadIncidents();
    connectToServer();
  }

  void _initializeNotifications() {
    flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();

    const AndroidInitializationSettings initializationSettingsAndroid =
    AndroidInitializationSettings('@drawable/app_icon.png');

    final InitializationSettings initializationSettings = InitializationSettings(
      android: initializationSettingsAndroid,
    );

    flutterLocalNotificationsPlugin.initialize(initializationSettings);
  }

  void _showNotification(int id, String title, String body) {
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
    AndroidNotificationDetails(
      'your_channel_id',
      'your_channel_name',
      importance: Importance.max,
      priority: Priority.high,
      ticker: 'ticker',
      visibility: NotificationVisibility.public,
      icon: '@drawable/app_icon',
    );

    const NotificationDetails platformChannelSpecifics = NotificationDetails(
      android: androidPlatformChannelSpecifics,
    );

    flutterLocalNotificationsPlugin.show(
      id,
      title,
      body,
      platformChannelSpecifics,
      payload: 'item x',
    );
  }

  void connectToServer() {
    socket = IO.io('http://192.168.100.15:5000', <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': true,
    });

    socket.on('connect', (_) {
      print('connected to server');
    });

    socket.on('alert', (data) {
      print('Alert received: $data');
      print('Data type: ${data.runtimeType}');

      if (data is Map<String, dynamic>) {
        notificationId++;
        String dateTime = DateFormat('yyyy-MM-dd – kk:mm').format(DateTime.now());

        setState(() {
          events.insert(0, {
            'event': data['event'] ?? 'N/A',
            'details': data['details'] ?? 'N/A',
            'time': dateTime,
          });
          _saveIncidents();
        });

        _showNotification(
          notificationId,
          'Alert',
          'Alert Type: ${data['event'] ?? 'N/A'}\nDetails: ${data['details'] ?? 'N/A'}\nTime: $dateTime',
        );
      } else {
        notificationId++;

        _showNotification(
          notificationId,
          'Alert',
          'Received unexpected data format',
        );
      }
    });

    socket.on('connect_error', (data) {
      print('Connection Error: $data');
    });

    socket.on('disconnect', (_) => print('disconnected from server'));
  }

  Future<void> _saveIncidents() async {
    final prefs = await SharedPreferences.getInstance();
    List<String> eventsList = events.map((event) => '${event['event']}|${event['details']}|${event['time']}').toList();
    await prefs.setStringList('events', eventsList);
  }

  Future<void> _loadIncidents() async {
    final prefs = await SharedPreferences.getInstance();
    List<String>? eventsList = prefs.getStringList('events');
    if (eventsList != null) {
      setState(() {
        events = eventsList.map((e) {
          final parts = e.split('|');
          return {
            'event': parts[0],
            'details': parts[1],
            'time': parts[2],
          };
        }).toList();
      });
    }
  }

  Future<void> _openNotificationSettings() async {
    const url = 'app-settings:';
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not open notification settings';
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Your App',
      theme: _isDarkMode ? ThemeData.dark() : ThemeData.light(), // Apply theme based on dark mode
      initialRoute: '/login',
      routes: {
        '/login': (context) => LoginPage(),
        '/signup': (context) => SignupPage(), // Add signup route
        '/forgot_password': (context) => ForgotPasswordPage(), // Add forgot password route
        '/dashboard': (context) => DashboardPage(title: 'Dashboard', events: events),
        '/incidents': (context) => IncidentsPage(events: events, onClear: () {
          setState(() {
            events.clear();
            _saveIncidents();
          });
        }),
        '/settings': (context) => SettingsPage(
          isDarkMode: _isDarkMode,
          onThemeChanged: (bool value) {
            setState(() {
              _isDarkMode = value;
            });
          },
          onOpenNotificationSettings: _openNotificationSettings,
        ),
      },
    );
  }

  @override
  void dispose() {
    socket.disconnect();
    super.dispose();
  }
}
