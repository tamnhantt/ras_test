import 'package:flutter/material.dart';
import 'package:process_run/process_run.dart';
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
      ProcessResult result = await Process.run(
        'python backend.py ${widget.sensorName} ${value.toString()}',
        [],
      );
      print("Python output: ${result.stdout}");
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
          min: 1,
          max: 5,
          divisions: 50,
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
