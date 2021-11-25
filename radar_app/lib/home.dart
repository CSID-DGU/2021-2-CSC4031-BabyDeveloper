import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'api.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final listenConditionController = Get.put(VmListenCondition());

  Timer? timer;

  @override
  void initState() {
    super.initState();
    timer = Timer.periodic(const Duration(seconds: 1),
        (Timer t) => listenConditionController.getCondition());
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Center(
          child: Text(
            "레이더 센서 정보",
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
      ),
      body: Center(
        child: GetBuilder(
          init: listenConditionController,
          builder: (_) => Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              (listenConditionController.condition == "safe")
                  ? SizedBox(
                      height: 359,
                      width: 300,
                      child: Image.asset("asset/safe-light.png"))
                  : (listenConditionController.condition == "danger")
                      ? SizedBox(
                          height: 359,
                          width: 300,
                          child: Image.asset("asset/warning-light.png"))
                      : (listenConditionController.condition == "noPerson")
                          ? SizedBox(
                              height: 359,
                              width: 300,
                              child: Image.asset("asset/light-off.png"))
                          : SizedBox(
                              height: 359,
                              width: 300,
                              child: Image.asset("asset/waiting.png"))
            ],
          ),
        ),
      ),
    );
  }
}
