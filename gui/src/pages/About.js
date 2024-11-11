import React from "react";
import { LargeTitle } from "../components/sidebar/styles";
import { TextContainer, HorizontalList, StyledLink } from "../components/layout/styles";

const About = () => {
    return (
        <TextContainer>
            <LargeTitle>About</LargeTitle><br />
            From the paper <i>“Global Geolocated Realtime Data of Interfleet 
            Urban Transit Bus Idling”</i>, GRD-TRT-BUF-4I (Ground Truth Buffer for Idling) 
            offers a global perspective on the emergent behavior of interfleet idling 
            patterns from worldwide urban transit bus operations. This work aims to 
            exhibit the issue's ubiquity and scale as a first step in reducing its 
            many negative impacts, including air pollution, ecological stress, 
            and economic inefficiency. Only after we measure and illustrate a 
            detailed and dynamic picture of the problem, can we actively address it. 
            We hope that this data helps to make our global communities healthier 
            and more sustainable, while lowering cost and increasing efficiency.
            <br /><br />

            <h4>Links</h4>
            <HorizontalList>
                <li>
                    Repo: <StyledLink href="https://www.github.com/nickkunz/idling">Github</StyledLink>
                </li>
                <li>
                    Preprint: <StyledLink href="https://arxiv.org/abs/2403.03489.pdf">arXiv</StyledLink>
                </li>
                <li>
                    Test Data: <StyledLink href="https://doi.org/10.6084/m9.figshare.25224224">figshare</StyledLink>
                </li>
            </HorizontalList><br/>

            <HorizontalList>
                <li>
                    <h4>Contacts</h4>
                    Nick Kunz<br/>
                    Cornell University<br/>
                    <StyledLink href="mailto:nhk37@cornell.edu">nhk37@cornell.edu</StyledLink><br/><br/>
                </li>
                <li>
                    <h4>&nbsp;</h4>
                    H. Oliver Gao<br/>
                    Cornell University<br/>
                    <StyledLink href="mailto:hg55@cornell.edu">hg55@cornell.edu</StyledLink><br/><br/>
                </li>
            </HorizontalList>

            <h4>References</h4>
                Kunz, N., Gao, H. O. (2024). Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling. Preprint. <i>arXiv:5451982</i>. <StyledLink href="https://arxiv.org/abs/2403.03489.pdf">https://arxiv.org/abs/2403.03489</StyledLink>.
        </TextContainer>
    );
};

export default About;