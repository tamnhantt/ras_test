import 'package:flutter/material.dart';
import 'package:gialap/FE/slider.dart';

void main() {
  runApp(const MyApp());
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
