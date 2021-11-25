import 'package:get/get.dart';

String url = "http://52.79.198.17:5000/";

class ListenCondition extends GetConnect {
  Future<Response> listenNotify() {
    return get(url + "listen_condition/");
  }
}


class VmListenCondition extends GetxController {
  String condition = "";

  void getCondition() async {
    var vmListenCondition = await ListenCondition().listenNotify();
    if (vmListenCondition.bodyString != null) {
      condition = vmListenCondition.bodyString!;
      update();
    }
  }

}