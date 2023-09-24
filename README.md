<!-- Improved compatibility of back to top link -->

<a name="top"></a>

<!-- PROJECT SHIELDS -->

[![MIT License][license-shield]][license]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#environments">Environments</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

# 🦜 ChatActor

The history-studying platform based on role-playing

Chat with your favorite Hero, Anime-Charactor, Actor ..

ChatActor can be enjoyed [here!](https://chatactor.streamlit.app/)

![main]

<!-- ABOUT THE PROJECT -->

## About the project

역사적 인물 (e.g. 이순신, 세종대왕)의 역할을 수행하는 ChatBot을 만들고 해당 ChatBot과 대화하며 자연스럽게 학습을 할 수 있는 플랫폼입니다.

Main contents는 다음과 같습니다.

- 캐릭터 선택 또는 학습이나 대화하고 싶은 캐릭터 생성
- 캐릭터와 자유롭게 대화하며 역사에 대한 학습을 진행
- 대화 내용을 기억하고 대화 내용을 바탕으로한 캐릭터의 자연스러운 질문을 통해 복습

ChatBot 구현 시 Prompt는 다음과 같은 부분을 신경썼습니다.

- 캐릭터 생성 시 DuckDuckGo, Wikipedia 등의 Search API를 활용하여 Profiler가 스스로 인물에 대한 정보를 스크래핑합니다.
- 생선된 캐릭터는 시대적 상황과 직책에 맞는 어조를 사용합니다.
- LLM 모델에서 흔히 볼 수 있는 환각 현상을 줄여 해당 캐릭터와 관련이 없는 인물 또는 사건에 대해 질문할 시 최대한 답하지 않도록 구현했습니다.
- 일정 대화가 오고간 후 대화의 내용을 바탕으로 ChatBot이 사용자에게 질문을 하여 학습 성취도를 평가합니다.

\*사용 시 🔑 OpenAI API 키가 필요합니다.

### Environments

| Types      | Contents                             |
| ---------- | ------------------------------------ |
| OS         | Ubuntu                               |
| Languages  | Python                               |
| Databases  | Faiss                                |
| Frameworks | OpenAI, LangChain, Streamlit, Poetry |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Getting Started -->

## Getting Started

```shell
git clone https://github.com/minocrafft/chatactor && cd chatactor

poetry shell

streamlit run main.py
```

<!-- Contributors -->

## Contributors

- Heonjin Kwon - [@kwon-evan](https://github.com/kwon-evan)
- Minho Kim - [@minocrafft](https://github.com/minocrafft)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/minocrafft/chatactor.svg?style=for-the-badge
[license]: LICENSE
[main]: assets/main.png
