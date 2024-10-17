import 'package:flutter/material.dart';

class IncidentsPage extends StatelessWidget {
  final List<Map<String, String>> events; // Receive events from MyApp
  final VoidCallback onClear;

  IncidentsPage({required this.events, required this.onClear});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Incidents'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: events.length,
              itemBuilder: (context, index) {
                final event = events[index];
                return ListTile(
                  leading: Icon(
                    Icons.error,
                    color: Colors.red, // Red color for the exclamation mark
                  ),
                  title: Text(event['event'] ?? 'N/A'),
                  subtitle: Text('${event['details'] ?? 'N/A'}\nTime: ${event['time'] ?? 'N/A'}'),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: ElevatedButton(
              onPressed: onClear,
              child: Text('Clear'),
            ),
          ),
        ],
      ),
    );
  }
}
