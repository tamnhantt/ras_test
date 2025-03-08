import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class SensorSlider extends StatefulWidget {
  final String sensorName;
  const SensorSlider({super.key, required this.sensorName});

  @override
  _SensorSliderState createState() => _SensorSliderState();
}

class _SensorSliderState extends State<SensorSlider> {
  double _currentSliderValue = 1;
  bool _isSending = false;
  String _responseMessage = "";

  Future<void> _sendDataToBackend(double value) async {
    setState(() {
      _isSending = true;
      _responseMessage = "Đang gửi dữ liệu...";
    });

    try {
      final response = await http.post(
        Uri.parse("http://127.0.0.1:5000/receive_data"), // Đổi thành IP Raspberry Pi nếu cần
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "sensorname": widget.sensorName,
          "value": value
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          _responseMessage = "Cập nhật thành công!";
        });
      } else {
        setState(() {
          _responseMessage = "Lỗi: ${response.body}";
        });
      }
    } catch (e) {
      setState(() {
        _responseMessage = "Không thể kết nối!";
      });
    } finally {
      setState(() {
        _isSending = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          "${widget.sensorName}: ${_currentSliderValue.toStringAsFixed(1)}",
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
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
          },
          onChangeEnd: (double value) {
            _sendDataToBackend(value);
          },
        ),
        _isSending
            ? CircularProgressIndicator()
            : Text(_responseMessage, style: TextStyle(color: Colors.green)),
        const Divider(),
      ],
    );
  }
}
