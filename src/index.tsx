import React, { useState, useEffect } from 'react';
import ReactDOM from "react-dom"
import Leaderboard from "./LeaderboardComp"

import "./index.css"

// import mockDataInfillingLightSpan from "./mocks/code_infilling_light_span.json"
// import mockDataInfillingMultiLine from "./mocks/code_infilling_multi_line.json"
// import mockDataInfillingSingleLine from "./mocks/code_infilling_single_line.json"
// import mockDataInfillingSpan from "./mocks/code_infilling_span.json"
// import mockDataComplete from "./mocks/code_complete.json"
// import mockDataExpalin from "./mocks/code_expalin.json"

import mockDataChineseEval from "./mocks/ifcodeeval_chinese_eval.json"
import mockDataEnglishEval from "./mocks/ifcodeeval_english_eval.json"


const LeaderboardTabs = () => {
  // State to track the currently selected tab
  const [activeTab, setActiveTab] = useState('tab1');
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // Function to render the leaderboard based on the selected tab
  const renderLeaderboard = () => {
    // console.log(activeTab);
    switch (activeTab) {
      case 'tab1':
        return <Leaderboard theme={{ base: "light" }} args={[mockDataEnglishEval, "English Evaluation"]} />;
      case 'tab2':
        return <Leaderboard theme={{ base: "light" }} args={[mockDataChineseEval, "Chinese Evaluation"]} />;
      default:
        return <div>Select a tab</div>;
    }
  };
  return (
    <div className="tabs-container">
      <ul className={`tabs ${isMobile ? 'mobile' : ''}`}>
        <li className={activeTab === 'tab1' ? 'is-active' : ''} onClick={() => setActiveTab('tab1')}><a>English Evaluation</a></li>
        <li className={activeTab === 'tab2' ? 'is-active' : ''} onClick={() => setActiveTab('tab2')}><a>Chinese Evaluation</a></li>
      </ul>
      <div className="tab-content">
        {renderLeaderboard()}
      </div>
    </div>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <section className="hero">
      <div className="hero-body">
        <div className="container is-fluid">
          <div className="columns  is-fullwidth">
            <div className="column has-text-centered is-fullwidth">
              <h1 className="title is-1 publication-title">
                IFEvalCode: Controlled Code Generation
              </h1>
              <div className="column has-text-centered">
                <div className="publication-links">
                  <span className="link-block">
                    <a href="."
                      className="external-link button is-normal is-rounded is-dark">
                      <span className="icon">
                        <i className="fas fa-file-pdf"></i>
                      </span>
                      <span>Paper (Coming Soon)</span>
                    </a>
                  </span>

                  <span className="link-block">
                    <a href="https://github.com/CSJianYang/IFEvalCode"
                      className="external-link button is-normal is-rounded is-dark">
                      <span className="icon">
                        <i className="fab fa-github"></i>
                      </span>
                      <span>Code (Coming Soon)</span>
                    </a>
                  </span>

                  <span className="link-block">
                    <a href="."
                      className="external-link button is-normal is-rounded is-dark">
                      <span className="icon">
                        <i className="far fa-images"></i>
                      </span>
                      <span>Evaluation Data (Coming Soon)</span>
                    </a>
                  </span>

                  <span className="link-block">
                    <a href="."
                      className="external-link button is-normal is-rounded is-dark">
                      <span className="icon">
                        <i className="far fa-images"></i>
                      </span>
                      <span>IFEvalCode-Instruct (Coming Soon)</span>
                    </a>
                  </span>

                  <span className="link-block">
                    <a
                      href="."
                      className="external-link button is-normal is-rounded is-dark"
                    >
                      <span className="icon">
                        <i className="fas fa-home"></i>
                      </span>
                      <span>Home</span>
                    </a>
                  </span>

                </div>
              </div>
              <div className="column has-text-centered">
                <LeaderboardTabs />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </React.StrictMode>,
  document.getElementById("root")
)