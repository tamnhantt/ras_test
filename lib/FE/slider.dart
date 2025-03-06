import 'package:flutter/material.dart';
import 'package:process_run/stdio.dart';

class SensorSlider extends StatefulWidget {
  final String sensorName;
  const SensorSlider({super.key, required this.sensorName});

  @override
  _SensorSliderState createState() => _SensorSliderState();
}

class _SensorSliderState extends State<SensorSlider> {
  double _currentSliderValue = 1;

  Future<void> _sendDataToPython(double value) async {
    try {
      String scriptPath = "python/out.py";
      ProcessResult result = await Process.run(
        'python3',
        [
          'out.py',
          widget.sensorName,
          value.toString(),
        ], // Truyền tham số đúng cách
      );
    } catch (e) {
      print("Error running Python script: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text("${widget.sensorName}: ${_currentSliderValue.toStringAsFixed(1)}"),
        Slider(
          value: _currentSliderValue,
          min: 0,
          max: 5,
          // divisions: 50,
          label: _currentSliderValue.toStringAsFixed(2),
          onChanged: (double value) {
            setState(() {
              _currentSliderValue = value;
            });
            _sendDataToPython(value);
          },
        ),
        const Divider(),
      ],
    );
  }
}
