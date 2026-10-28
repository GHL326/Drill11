# Boy 상태 다이어그램

```mermaid
stateDiagram-v2
    [*] --> IDLE
    IDLE: 진입 시 5초 타이머 및 프레임 초기화
    SLEEP: 누운 자세로 정지
    IDLE --> SLEEP: 5초 경과
    SLEEP --> IDLE: 스페이스 키 누름
    RUN: 단일 상태에서 좌우 이동
    RUN: 화면 경계에서 위치 제한
    IDLE --> RUN: 좌우 방향키 누름
    RUN --> RUN: 방향 변경
    RUN --> IDLE: 방향키 모두 놓음
    SLEEP --> RUN: 좌우 방향키 누름
    AUTORUN: AutoRun 클래스 / 2배 확대
    AUTORUN: 가까운 벽부터 이동 후 양쪽 벽 왕복
    AUTORUN: 종료 시 원래 크기 복구
    IDLE --> AUTORUN: A 키 누름
    SLEEP --> AUTORUN: A 키 누름
    RUN --> AUTORUN: A 키 누름
    AUTORUN --> AUTORUN: 벽 도착 / 반대 방향으로 이동
    AUTORUN --> IDLE: 시작 후 5초 경과
    AUTORUN --> RUN: 좌우 방향키 누름 / 자동 이동 취소
```

IDLE에 진입할 때마다 5초 타이머를 새로 시작합니다.
RUN은 좌우 공통 상태이며 `face_dir`로 방향을 구분합니다.
방향키를 모두 놓으면 IDLE로 돌아갑니다.
양쪽 방향키를 누르면 마지막에 누른 방향을 우선합니다.
SLEEP에서도 IDLE과 같은 방향키 처리로 RUN에 진입합니다.
A는 IDLE, SLEEP, RUN에서 동작하며 AUTORUN 중 다시 눌러도 타이머를 초기화하지 않습니다.
양쪽 벽까지 거리가 같으면 왼쪽 벽으로 먼저 이동합니다.
확대 시에도 캐릭터 전체가 화면 안에 있도록 위치를 제한합니다.
AUTORUN에서 방향키를 놓는 것만으로 취소되지 않으며, 방향키를 누르면 RUN으로 전환합니다.
자동 이동 종료 후 IDLE의 5초 수면 타이머를 새로 시작합니다.
