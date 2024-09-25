%% Perceptual DM - Wk7-S3 - DDM 
% 25 Sep 2024 

%% 
load Wk7S3DDMvisualization.mat

%% Section1: Choice 'Left' (Single Trial) 
% Bounds = +/- 10; (Left/Rt) 
% Starting pt = 0;
% Mean of the moment-by-moment evidence = 0.1;
% Variability (Std dev) evidence = 1; 


figure (1) 
plot(data1, '-b', 'LineWidth', 2);
axis([0 length(data1) -bound-2 bound+2]);
hold on
plot([0 length(data1)],[bound bound],'k-', 'LineWidth', 1.5);
plot([0 length(data1)],[-bound -bound],'k-', 'LineWidth', 1.5);
plot([0 length(data1)],[0 0],'k:', 'LineWidth', 1.5); % equal evidence

text(5, 9, 'Left');text(5, -9, 'Right');
text(45, -5, ['Reaction Time (RT) = ' num2str(length(data1)) 'ms']);

xlabel('Time (ms)');
ylabel('Decision variable (a.u.)');
title('Section1: Choice Left (Single Trial); mean=0.1, sd=1');
hold off 

%% Section2: Choice 'Left' (Single Trial with less noise in evidence accumulation) 
%% better than Q1 since noise is less as the standard deviation is less
figure (2) 
plot(data2, '-b', 'LineWidth', 2);
axis([0 length(data2) -bound-2 bound+2]);
hold on
plot([0 length(data2)],[bound bound],'k-', 'LineWidth', 1.5);
plot([0 length(data2)],[-bound -bound],'k-', 'LineWidth', 1.5);
plot([0 length(data2)],[0 0],'k:', 'LineWidth', 1.5); % equal evidence

text(5, 9, 'Left');text(5, -9, 'Right');
text(15, -5, ['Reaction Time (RT) = ' num2str(length(data2)) 'ms']);

xlabel('Time (ms)');
ylabel('Decision variable (a.u.)');
title('Section2: Choice Left (Single Trial); mean=0.1, sd=0.5');
hold off 


%% Section3: Choice 'Left' (Single Trial with greater mean evidence accumulation) 
 %% since data is more since mean is double therfore it is running better than . Q1 more linear
figure (3) 
plot(data3, '-b', 'LineWidth', 2);
axis([0 length(data3) -bound-2 bound+2]);
hold on
plot([0 length(data3)],[bound bound],'k-', 'LineWidth', 1.5);
plot([0 length(data3)],[-bound -bound],'k-', 'LineWidth', 1.5);
plot([0 length(data3)],[0 0],'k:', 'LineWidth', 1.5); % equal evidence

text(5, 9, 'Left');text(5, -9, 'Right');
text(15, -5, ['Reaction Time (RT) = ' num2str(length(data3)) 'ms']);

xlabel('Time (ms)');
ylabel('Decision variable (a.u.)');
title('Section3: Choice Left (Single Trial); mean=0.2, sd=1');
hold off 

%% Section4: Choice 'Left' (Multiple Trials) 
%% for 100 trials accuracy is 81 and avg reaction time is 68ms
% plot the trial
n=100;
correctRT = [];
errorRT = [];
nCorrect = 0;
nError = 0;
figure(4)
hold on
for ii = 1:n
    thisData = data4{ii,1};
    plot(thisData);%drawnow
    % if it was correct
    if  thisData(end)>bound
        % then keep score
        nCorrect = nCorrect+1;
        correctRT(end+1) = length(thisData);
    else
        nError = nError + 1;
        errorRT(end+1) = length(thisData);
    end
end

plot([0 350],[bound bound],'k-', 'LineWidth', 1.5);
plot([0 350],[-bound -bound],'k-', 'LineWidth', 1.5);
plot([0 350],[0 0],'k:', 'LineWidth', 1.5); % equal evidence

text(5, 9, 'Left');text(5, -9, 'Right');

pc = (nCorrect/n)*100; pe = (nError/n)*100; medcorRT = median(correctRT);
text(150, -3, ['% Corr Trials = ' num2str(pc)]);
text(150, -5, ['% Err Trials = ' num2str(pe)]);
text(150, -7, ['Med. Cor Reaction Time (RT) = ' num2str(medcorRT) 'ms']);


ylim([-10 10])
xlabel('Time (ms)');
ylabel('Decision variable (a.u.)');
title('Section4: Choice Left (100 Trials); mean=0.1, sd=1');


% Visualize the distribution of RT from correct trials in the inset 
axes('Position',[.7 .7 .2 .2])
box on
hist(correctRT,30);
ylabel('Freq');
xlabel('RT (ms)'); text(70, 140, 'Dist: Correct RT');
hold off

%% Section5:  Fit % correct and mean reaction times (Analytical solution)
% Given bounds Left and Right and a Gaussian process with a mean and std, 
% the probability that the process will end at the Left bound instead of the Right bound. The solution is the
% Shadlen equation 

%% as the mean evidence increasese the probability correct increases and the reaction time decreses

figure(5)
subplot(1,2,1)

hold on
plot(data5.meanEvidence,1./(1+exp(-data5.meanEvidence*data5.Bound )),'-b', 'LineWidth', 2);
xlabel('Mean evidence');
ylabel('Prob correct');
title('Section5: ProbCor vs MeanEv');
hold off 


subplot(1,2,2)
hold on
plot(data5.meanEvidence,(data5.Bound*100./data5.meanEvidence).*tanh(data5.meanEvidence*(data5.Bound*100)), '-b', 'LineWidth', 2);
xlabel('Mean evidence');
ylabel('RT (ms)'); 
title('Section5: RT vs MeanEv');
hold off

%% Section 6: MT neuron study data 


lb = {'Coh1', 'Coh11', 'Coh21', 'Coh31'};
sp = [0, 3, 6, 9];

% plot it
figure(6) 
for ii = 1:4
thisData = data6{1,ii};
hold on 
plot(thisData, 'LineWidth', 1.5);
text(1500, 15-sp(ii), ['RT' lb{ii} '=' num2str(length(thisData)) 'ms']);
end 

plot([0 3000],[22.8 22.8],'k-', 'LineWidth', 1.5);
plot([0 3000],[-22.8 -22.8],'k-', 'LineWidth', 1.5);
plot([0 3000],[0 0],'k:', 'LineWidth', 1.5);
text(550, 10, 'Left');text(550, -10, 'Right');

axis([0 3000 -22.8-2 22.8+2]);

legend('Coh1', 'Coh11', 'Coh21', 'Coh31', '', '', 'Location', 'southeast')
legend box off 

xlabel('Time (ms)');
ylabel('Decision variable (a.u.)');
title('Section6: Evidence accumulation in six motion coherences');
