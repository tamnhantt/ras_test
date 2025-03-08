import 'dart:io';
import 'package:flutter/material.dart';
import 'package:gialap/FE/slider.dart';

void main() {
  runApp(const MyApp());
  startBackend(); // Chạy backend khi ứng dụng khởi động
}

// Hàm chạy out.py (chỉ chạy nếu chưa chạy)
void startBackend() async {
  try {
    // Kiểm tra nếu backend chưa chạy, thì mới khởi động
    ProcessResult result = await Process.run('pgrep', ['-f', 'out.py']);
    if (result.stdout.toString().trim().isEmpty) {
      print("Khởi động backend...");
      Process.start('python3', ['out.py']);
    } else {
      print("Backend đã chạy, không cần khởi động lại.");
    }
  } catch (e) {
    print("Lỗi khi khởi động backend: $e");
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sensor Sliders',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const SensorSliderPage(),
    );
  }
}

class SensorSliderPage extends StatelessWidget {
  const SensorSliderPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sensor Sliders')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            SensorSlider(sensorName: "Engine Speed Sensor"),
            SensorSlider(sensorName: "Camshaft Position Sensor"),
          ],
        ),
      ),
    );
  }
}
