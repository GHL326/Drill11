# Boy 상태 다이어그램

```mermaid
stateDiagram-v2
    [*] --> IDLE
    IDLE: 진입 시 5초 타이머 및 프레임 초기화
    SLEEP: 누운 자세로 정지
    IDLE --> SLEEP: 5초 경과
    SLEEP --> IDLE: 스페이스 키 누름
```

IDLE에 진입할 때마다 5초 타이머를 새로 시작합니다.
