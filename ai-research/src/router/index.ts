import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Home from '../components/Home.vue';
import WritingTools from '../views/WritingTools.vue';
import MasterThesisProposalOutline from '../views/MasterThesisProposalOutline.vue';
import JournalSubmission from '../views/JournalSubmission.vue';
import NatureGeneticsSubmission from '../views/NatureGeneticsSubmission.vue';
import NatureCommunicationsSubmission from '../views/NatureCommunicationsSubmission.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
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
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router; 