

정의해야 할 부분



chaincode의 'name'.json은 각 계약에 관련된 정보를 정의 - 스마트 컨트랙트 파일
chaincode/ledger 에는 'name'.json와 이름이 같은 실제 거래내역을 저장 - 원장 파일

통신은 기본적으로 grpc를 통해서 하기 때문에 기본적으로 각 거래에 필요한 속성들을 proto3을 이용하여 정의하고
네트워크(채널)를 만든다.
network_interface/grpc의 foodchain.proto에는 메시지 형식과 함를 정의함.
이후에 set.py를 실행시키면 foodchain_pb2.py와 foodchain_pb2_grpc.py가 생성됨.

이를 바탕으로 server.py와 client.py를 생성시킬 수 있다.
필요한 IP와 PORT는 위에서 정의된 스마트 컨트랙트 파일에서 가져올 수 있다. - FMS에 요청을 안해도 됨.

ledger_interface에는 기본적인 인터페이스만 정의하고 이를 재정의하는 부분은 core의 makeLedger.py 다.


기존의 toJson, fromJson과는 다르게 클래스 내 속성을 자유롭게 정의할 수 있도록 소스를 변경함.

파이썬 상에서는 자유롭게 추가, 변경이 가능하지만 grpc를 이용하면서 정의되있는 부분이 있기 때문에 저장되는 데이터는 정형적이다.

grpc를 수행시키기 위해서는 파이썬 2.7 또는 3.4 이상의 버전이 필요하다.
python -m pip install grpcio grpcio-tools

현재 소스의 grpc 연결방식은 server-client방식의 전형적인 소켓 형식이지만 
기본적으로 grpc에서 양방향 스트리밍 방식의 통신을 지원하기 때문에 p2p를 만들때 유용할 수 있다.


폴더 구조

chaincode			- 스마트 컨트랙트 파일을 저장
					- ledger	- 스마트 컨트랙트 파일의 원장을 저장

core				- run.py에 실질적으로 필요한 함수들을 정의함.

crypto				- 전자봉투 모듈
					- keys		- 스마트 컨트랙트에 해당하는 노드의 공개키 저장

ledger_interface	- 클래스 인터페이스 정의

network_interface	- grpc나 기타 통신 프로토콜 정의



3줄 요약
1. transaction에 toJson, fromJson함수를 유동적으로 바꿈. - 클래스 변수를 추가할 수 있음.
2. 스마트 컨트랙트를 위해서 정의해야 할 부분이 생김 - chaincode의 json파일, grpc의 proto파일, set.sh 실행
3. 최종적으로 하나의 파일만 실행시킬 수 있도록 run.py에 종합.


