import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import WritingTools from '../views/WritingTools.vue';
import MasterThesisProposalOutline from '../views/MasterThesisProposalOutline.vue';
import JournalSubmission from '../views/JournalSubmission.vue';
import NatureGeneticsSubmission from '../views/NatureGeneticsSubmission.vue';
import NatureCommunicationsSubmission from '../views/NatureCommunicationsSubmission.vue';
import ReviewWriting from '../views/ReviewWriting.vue';
import MolecularBiology from '../views/MolecularBiology.vue';
import ProjectReview from '../views/ProjectReview.vue';
import FundProjectReview from '../views/FundProjectReview.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
    children: [
      {
        path: 'collaboration',
        name: 'WritingTools',
        component: WritingTools
      },
      {
        path: 'journal-submission',
        name: 'JournalSubmission',
        component: JournalSubmission
      },
      {
        path: 'review-writing',
        name: 'ReviewWriting',
        component: ReviewWriting
      },
      {
        path: 'project-review',
        name: 'ProjectReview',
        component: ProjectReview
      }
    ]
  },
  {
    path: '/thesis-outline',
    name: 'MasterThesisProposalOutline',
    component: MasterThesisProposalOutline
  },
  {
    path: '/nature-genetics-submission',
    name: 'NatureGeneticsSubmission',
    component: NatureGeneticsSubmission
  },
  {
    path: '/nature-communications-submission',
    name: 'NatureCommunicationsSubmission',
    component: NatureCommunicationsSubmission
  },
  {
    path: '/molecular-biology',
    name: 'MolecularBiology',
    component: MolecularBiology
  },
  {
    path: '/fund-project-review',
    name: 'FundProjectReview',
    component: FundProjectReview
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router; 