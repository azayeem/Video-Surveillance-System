import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  final bool isDarkMode;
  final ValueChanged<bool> onThemeChanged;
  final VoidCallback onOpenNotificationSettings;

  SettingsPage({
    required this.isDarkMode,
    required this.onThemeChanged,
    required this.onOpenNotificationSettings,
  });

  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Settings'),
      ),
      body: ListView(
        padding: EdgeInsets.all(16.0),
        children: [
          SwitchListTile(
            title: Text('Dark Mode'),
            value: widget.isDarkMode,
            onChanged: (bool value) {
              widget.onThemeChanged(value);
            },
          ),
          ListTile(
            title: Text('Notification Settings'),
            subtitle: Text(''),
            onTap: () {
              widget.onOpenNotificationSettings();
            },
          ),
          // Add more settings options here
          ListTile(
            title: Text('About'),
            subtitle: Text('Video Survellance System Mobile Application'),
            onTap: () {
              // Handle "About" option here
            },
          ),
          // Add any additional settings options as needed
        ],
      ),
    );
  }
}
